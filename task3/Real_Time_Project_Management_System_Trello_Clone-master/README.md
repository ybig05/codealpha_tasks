📋 Project Management Tool (Trello Clone)
🧠 Overview

This project is a full-featured collaborative project management system inspired by tools like Trello and Asana.

It allows users to create projects, manage tasks, collaborate with team members, and track progress using a Kanban-style board with real-time updates.

✨ Features
🔐 Authentication System
User signup and login
Persistent sessions using localStorage
Multi-user demo accounts
Secure logout functionality
📊 Project Management
Create and manage multiple projects
Add/remove team members by email
Project descriptions and metadata
Delete projects with confirmation
📋 Kanban Board
4 workflow stages:
To Do
In Progress
Review
Done
Drag-and-drop task movement
Task counters per column
Visual priority labels
✅ Task Management
Create, edit, and delete tasks
Assign tasks to team members
Priority levels:
High 🔴
Medium 🟡
Low 🟢
Task detail modal for full editing
Move tasks across workflow stages
💬 Comments & Collaboration
Add comments to tasks
Real-time comment updates
User avatars and timestamps
Comment counters on task cards
🔔 Notifications System
Real-time notifications panel
Unread notification badges
Activity tracking:
Task creation
Updates
Comments
Clear all notifications feature
“Time ago” formatting
🌐 Real-Time Updates
WebSocket-based architecture
Live connection status indicator
Auto-reconnection on disconnect
Event-driven updates (tasks, comments)
Ready for integration with Socket.IO
🎨 UI/UX Design
Modern dark theme
Responsive layout
Smooth animations and transitions
Clean typography (Manrope font)
Custom scrollbars and gradient accents
🏗️ Architecture
Frontend
Built with vanilla JavaScript (no frameworks)
Centralized state management (AppState pattern)
Event-driven architecture
LocalStorage for data persistence
Backend (In Progress)
Planned integration with:
Node.js
Express
MongoDB
RESTful API structure
JWT-based authentication
Real-time updates via WebSockets
🔑 Demo Credentials
Email: john@example.com  
Password: password

Other demo users:

jane@example.com
mike@example.com
🚀 Getting Started
1. Clone the repository
git clone https://github.com/YOUR_USERNAME/codealpha_tasks.git
2. Navigate to the project
cd task2_project_management_tool
3. Run the application

Simply open the index.html file in your browser
OR use Live Server in VS Code

🔮 Future Improvements
Full backend integration
Role-based access control (Admin/User)
Task deadlines and calendar view
Search and filtering
File attachments
Deployment (cloud hosting)
💼 Use Case

This project demonstrates:

Full-stack system design principles
Real-time application architecture
Frontend state management
Scalable and modular code structure
🧑‍💻 Author

Iradukunda Girukwishaka
