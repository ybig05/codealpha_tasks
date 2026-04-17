from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Profile, Post, Comment, Like, Follow
from .serializers import (
    UserSerializer, RegisterSerializer, ProfileSerializer,
    PostSerializer, CommentSerializer
)


# ── Auth ──────────────────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user, context={'request': request}).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user, context={'request': request}).data
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout(request):
    request.user.auth_token.delete()
    return Response({'message': 'Logged out successfully'})


@api_view(['GET'])
def me(request):
    return Response(UserSerializer(request.user, context={'request': request}).data)


# ── Users / Profiles ──────────────────────────────────────────────────────────

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = User.objects.all().select_related('profile')
        q = self.request.query_params.get('q')
        if q:
            qs = qs.filter(username__icontains=q)
        return qs


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all().select_related('profile')
    serializer_class = UserSerializer
    lookup_field = 'username'


@api_view(['PATCH'])
def update_profile(request):
    profile = request.user.profile
    # update User fields
    user = request.user
    for field in ['first_name', 'last_name', 'email']:
        if field in request.data:
            setattr(user, field, request.data[field])
    user.save()
    # update Profile fields
    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(UserSerializer(user, context={'request': request}).data)


# ── Follow ────────────────────────────────────────────────────────────────────

@api_view(['POST'])
def follow_user(request, username):
    target = get_object_or_404(User, username=username)
    if target == request.user:
        return Response({'error': "You can't follow yourself"}, status=400)
    follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
    if not created:
        follow.delete()
        return Response({'following': False, 'message': f'Unfollowed {username}'})
    return Response({'following': True, 'message': f'Following {username}'})


@api_view(['GET'])
def user_followers(request, username):
    user = get_object_or_404(User, username=username)
    followers = User.objects.filter(following__following=user)
    return Response(UserSerializer(followers, many=True, context={'request': request}).data)


@api_view(['GET'])
def user_following(request, username):
    user = get_object_or_404(User, username=username)
    following = User.objects.filter(followers__follower=user)
    return Response(UserSerializer(following, many=True, context={'request': request}).data)


# ── Posts ─────────────────────────────────────────────────────────────────────

class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        feed = self.request.query_params.get('feed')
        if feed and self.request.user.is_authenticated:
            following_ids = Follow.objects.filter(
                follower=self.request.user
            ).values_list('following_id', flat=True)
            return Post.objects.filter(
                author_id__in=list(following_ids) + [self.request.user.id]
            ).select_related('author', 'author__profile').prefetch_related('comments__author', 'comments__author__profile')
        return Post.objects.all().select_related('author', 'author__profile').prefetch_related('comments__author', 'comments__author__profile')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all().select_related('author', 'author__profile').prefetch_related('comments__author')
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    def perform_update(self, serializer):
        if self.get_object().author != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only edit your own posts.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only delete your own posts.")
        instance.delete()


@api_view(['GET'])
def user_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).select_related('author', 'author__profile').prefetch_related('comments__author')
    serializer = PostSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)


# ── Likes ─────────────────────────────────────────────────────────────────────

@api_view(['POST'])
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        return Response({'liked': False, 'likes_count': post.likes_count()})
    return Response({'liked': True, 'likes_count': post.likes_count()})


# ── Comments ──────────────────────────────────────────────────────────────────

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)


@api_view(['DELETE'])
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return Response({'error': 'Permission denied'}, status=403)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
