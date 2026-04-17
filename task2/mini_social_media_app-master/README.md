# ✦ Pulse — Mini Social Media App

A full-stack social media app with Django REST backend and vanilla JS frontend.

## Features
- 🔐 User registration & login (Token auth)
- 👤 User profiles with bio, location, website
- 📝 Create, view, delete posts
- 💬 Comment on posts
- ❤️ Like / unlike posts
- 👥 Follow / unfollow users
- 🔍 Live user search
- 📰 Personalized feed (shows posts from people you follow)

## Project Structure
```
socialmedia/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── socialmedia/          # Django project settings
│   │   ├── settings.py
│   │   └── urls.py
│   └── api/                  # Main app
│       ├── models.py         # User, Profile, Post, Comment, Like, Follow
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
└── frontend/
    └── index.html            # Standalone SPA (no build step)
```

## Database Schema
- **User** (Django built-in)
- **Profile** — OneToOne with User; bio, avatar, location, website
- **Post** — author (FK User), content, image, timestamps
- **Comment** — post (FK), author (FK), content
- **Like** — post (FK), user (FK) — unique together
- **Follow** — follower (FK), following (FK) — unique together

## Quick Start

### 1. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Run migrations
```bash
python manage.py migrate
```

### 3. (Optional) Seed demo data
```bash
bash ../setup.sh
# Creates users: alice, bob, cara — all with password: password123
```

### 4. Start the backend
```bash
python manage.py runserver
# API running at http://localhost:8000/api/
```

### 5. Open the frontend
Simply open `frontend/index.html` in your browser.
No build step required — it's plain HTML + CSS + JS.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login, receive token |
| POST | `/api/auth/logout/` | Logout |
| GET | `/api/auth/me/` | Current user info |
| GET | `/api/users/` | List / search users |
| GET | `/api/users/:username/` | User profile |
| PATCH | `/api/profile/update/` | Update own profile |
| POST | `/api/users/:username/follow/` | Toggle follow |
| GET | `/api/users/:username/followers/` | List followers |
| GET | `/api/users/:username/following/` | List following |
| GET/POST | `/api/posts/` | List all posts / create post |
| GET | `/api/posts/?feed=true` | Personal feed |
| GET/DELETE | `/api/posts/:id/` | Post detail / delete |
| POST | `/api/posts/:id/like/` | Toggle like |
| POST | `/api/posts/:id/comments/` | Add comment |
| DELETE | `/api/comments/:id/` | Delete comment |

## Authentication
All protected endpoints require the header:
```
Authorization: Token <your-token>
```

## Tech Stack
- **Backend**: Django 4.2, Django REST Framework, SQLite
- **Auth**: DRF Token Authentication
- **Frontend**: Vanilla HTML/CSS/JavaScript (zero dependencies, no build step)
- **Database**: SQLite (easily swappable to PostgreSQL)
