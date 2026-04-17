from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/logout/', views.logout, name='logout'),
    path('auth/me/', views.me, name='me'),

    # Users
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<str:username>/', views.UserDetailView.as_view(), name='user-detail'),
    path('users/<str:username>/posts/', views.user_posts, name='user-posts'),
    path('users/<str:username>/follow/', views.follow_user, name='follow-user'),
    path('users/<str:username>/followers/', views.user_followers, name='user-followers'),
    path('users/<str:username>/following/', views.user_following, name='user-following'),

    # Profile
    path('profile/update/', views.update_profile, name='update-profile'),

    # Posts
    path('posts/', views.PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/like/', views.toggle_like, name='toggle-like'),
    path('posts/<int:post_id>/comments/', views.CommentCreateView.as_view(), name='comment-create'),

    # Comments
    path('comments/<int:comment_id>/', views.delete_comment, name='comment-delete'),
]
