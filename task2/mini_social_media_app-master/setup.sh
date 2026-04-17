#!/bin/bash
# ─────────────────────────────────────────────
#  Pulse Social Media — Quick Setup Script
# ─────────────────────────────────────────────

echo "🚀 Setting up Pulse Social Media Backend..."

cd "$(dirname "$0")/backend"

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser (optional - interactive)
echo ""
echo "Would you like to create an admin superuser? (y/n)"
read -r answer
if [ "$answer" = "y" ]; then
    python manage.py createsuperuser
fi

# Seed some demo data (optional)
echo ""
echo "Would you like to seed demo data? (y/n)"
read -r answer
if [ "$answer" = "y" ]; then
    python manage.py shell << 'PYEOF'
from django.contrib.auth.models import User
from api.models import Post, Comment, Like, Follow

# Create demo users
users_data = [
    {'username': 'alice', 'email': 'alice@example.com', 'first_name': 'Alice', 'last_name': 'Chen'},
    {'username': 'bob',   'email': 'bob@example.com',   'first_name': 'Bob',   'last_name': 'Rivera'},
    {'username': 'cara',  'email': 'cara@example.com',  'first_name': 'Cara',  'last_name': 'Smith'},
]

users = []
for ud in users_data:
    u, created = User.objects.get_or_create(username=ud['username'], defaults=ud)
    if created:
        u.set_password('password123')
        u.save()
        u.profile.bio = f"Hey, I'm {ud['first_name']}! Welcome to my profile."
        u.profile.location = "San Francisco, CA"
        u.profile.save()
    users.append(u)

alice, bob, cara = users

# Follows
Follow.objects.get_or_create(follower=bob,  following=alice)
Follow.objects.get_or_create(follower=cara, following=alice)
Follow.objects.get_or_create(follower=alice, following=bob)

# Posts
posts_data = [
    (alice, "Just launched my new portfolio site! 🎉 Spent the last month building it from scratch. Let me know what you think!"),
    (bob,   "Morning hike done ✅ There's something magical about being on a trail before sunrise. Highly recommend it."),
    (cara,  "Currently reading 'Thinking, Fast and Slow' by Kahneman. Mind = blown 🤯 Any other book recommendations?"),
    (alice, "Hot take: tabs > spaces. Fight me 👀 #DevLife"),
    (bob,   "Made homemade pasta for the first time tonight. It was messier than I expected but SO worth it 🍝"),
]

created_posts = []
for author, content in posts_data:
    p, _ = Post.objects.get_or_create(author=author, content=content)
    created_posts.append(p)

# Likes
Like.objects.get_or_create(post=created_posts[0], user=bob)
Like.objects.get_or_create(post=created_posts[0], user=cara)
Like.objects.get_or_create(post=created_posts[1], user=alice)
Like.objects.get_or_create(post=created_posts[2], user=alice)
Like.objects.get_or_create(post=created_posts[2], user=bob)

# Comments
Comment.objects.get_or_create(post=created_posts[0], author=bob,  content="Looks awesome Alice! The animations are super smooth 🔥")
Comment.objects.get_or_create(post=created_posts[0], author=cara, content="Love the colour palette you chose!")
Comment.objects.get_or_create(post=created_posts[2], author=alice, content="'Atomic Habits' by James Clear is another great read! Changed how I think about productivity.")

print("✅ Demo data created! Login with: alice / password123")
PYEOF
fi

echo ""
echo "✅ Setup complete!"
echo "▶  Run the server:  cd backend && python manage.py runserver"
echo "📖 API base URL:    http://localhost:8000/api/"
echo "🔧 Admin panel:     http://localhost:8000/admin/"
echo "🌐 Open frontend/index.html in your browser to use the app"
