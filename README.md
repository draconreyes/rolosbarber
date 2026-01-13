# 💈 Barbershop Appointment Management System

A full-stack web application for managing barbershop appointments with role-based access control, built with modern technologies and containerized with Docker.

---

## 📋 Table of Contents

- [Purpose](#-purpose)
- [Technologies](#-technologies)
- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Purpose

This application was developed to streamline the appointment booking process for barbershops. It provides:

- **For Clients**: An easy-to-use interface to book appointments, view available time slots, and manage their bookings
- **For Administrators**: A comprehensive dashboard to manage all appointments, view client details, and control appointment statuses
- **For Business**: A complete solution to reduce no-shows, optimize scheduling, and improve customer service

The system eliminates double-booking issues, provides real-time availability, and enables efficient appointment management through a modern web interface.

---

## 🛠️ Technologies

### Backend
- **Python 3.11** - Programming language
- **Django 4.2 LTS** - Web framework
- **Django REST Framework 3.14** - RESTful API toolkit
- **PostgreSQL 15** - Relational database
- **SimpleJWT** - JWT authentication
- **pytest** - Testing framework

### Frontend
- **Angular 17** - Frontend framework
- **TypeScript 5.2** - Type-safe JavaScript


### DevOps & Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

---

## ✨ Features

### 🔐 Authentication & Authorization
- JWT-based authentication with access and refresh tokens
- Role-based access control (Admin/Client)
- Secure password validation
- Protected routes with guards

### 👤 Client Features
- User registration and login
- View available time slots (8 AM - 8 PM)
- Book appointments with service selection
- View personal appointment history
- Cancel own appointments
- Real-time slot availability

### 👨‍💼 Admin Features
- View all appointments across all clients
- Filter appointments by date
- View today's appointments dashboard
- See detailed client information (name, email, phone)
- Confirm or cancel appointments
- Expandable appointment details
- Access to Django admin panel

### 📅 Appointment Management
- Prevent double-booking (unique time slots)
- Three service types: Haircut, Beard, Combo
- Three status types: Pending, Confirmed, Canceled
- Optional notes for special requests
- Date and time validation

### 🎨 User Interface
- Responsive design
- Intuitive navigation
- Real-time updates
- Color-coded status indicators
- Clean and modern UI

---
## 📦 Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software

1. **Docker Desktop**
   - Version: 20.10 or higher
   - Download: https://www.docker.com/products/docker-desktop
   - Verify installation:
     ```bash
     docker --version
     docker compose version
     ```

2. **Git** (optional, for cloning)
   - Version: 2.0 or higher
   - Download: https://git-scm.com/downloads

### System Requirements

- **OS**: Windows 10/11 (with WSL2), macOS, or Linux
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: At least 2GB free space
- **Ports**: 4200, 8000, and 5432 must be available

---

## 🚀 Installation & Setup

### Step 1: Clone or Download the Project

```bash
# Option A: Clone with Git
git clone <repository-url>
cd rolosbarber

# Option B: Download and extract ZIP
# Then navigate to the project folder
cd rolosbarber
```

### Step 2: Verify Project Structure

Ensure your project has the following structure:

```
rolosbarber/
├── backend/
│   ├── barbershop/
│   ├── users/
│   ├── appointments/
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

### Step 3: Configure Environment Variables (Optional)

The application works with default settings, but you can customize them:

1. Create a `.env` file in the `backend/` directory:

```bash
cd backend
touch .env  # On Windows: type nul > .env
```

2. Add your custom configuration:

```env
SECRET_KEY=your-custom-secret-key-here
DEBUG=True
DATABASE_NAME=barbershop_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=db
DATABASE_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:4200
```

### Step 4: Build and Start the Application

From the project root directory (`rolosbarber/`):

```bash
# Build and start all containers
docker compose up --build
```

**What happens during this step:**
1. Downloads base images (Python, Node, PostgreSQL, Nginx)
2. Builds the backend container with Django
3. Builds the frontend container with Angular
4. Creates a PostgreSQL database
5. Runs database migrations
6. Starts all services

**Expected output:**
```
[+] Building 45.2s
[+] Running 3/3
 ✔ Container barbershop_db        Started
 ✔ Container barbershop_backend   Started
 ✔ Container barbershop_frontend  Started
```

**Wait for these messages:**
```
barbershop_backend   | Django version 4.2.11, using settings 'barbershop.settings'
barbershop_backend   | Starting development server at http://0.0.0.0:8000/
barbershop_frontend  | nginx/1.29.4
```

### Step 5: Create an Admin User

Open a **new terminal** (keep the previous one running) and execute:

```bash
# Create a superuser for Django admin panel
docker exec -it barbershop_backend python manage.py createsuperuser
```

Follow the prompts:
```
Username: admin
Email address: admin@barbershop.com
Password: ******** (minimum 8 characters)
Password (again): ********
Superuser created successfully.
```

### Step 6: Create an Admin User for the Application

Now create an admin user with the 'admin' role for the barbershop application:

```bash
docker exec -it barbershop_backend python -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='barbershop_admin').exists():
    User.objects.create_user(
        username='barbershop_admin',
        email='admin@barbershop.com',
        password='admin123',
        role='admin',
        first_name='Admin',
        last_name='Barbershop',
        phone='1234567890'
    )
    print('Admin user created successfully!')
else:
    print('Admin user already exists.')
"
```

### Step 7: Verify Installation

Open your browser and check:

1. **Frontend Application**: http://localhost:4200
   - Should show the login page

2. **Backend API**: http://localhost:8000/api/appointments/
   - Should show "Authentication credentials were not provided"

3. **Django Admin Panel**: http://localhost:8000/admin
   - Login with the superuser credentials created in Step 5

---

## 📖 Usage

### For Clients

#### 1. Register a New Account

1. Go to http://localhost:4200
2. Click "Register"
3. Fill in the form:
   - Username: `john_client`
   - Email: `john@example.com`
   - Password: `password123`
   - Phone: `5551234567`
4. Click "Register"
5. You'll be redirected to login

#### 2. Login

1. Enter your credentials
2. Click "Login"
3. You'll be redirected to `/appointments/my_appointments`

#### 3. Create an Appointment

1. Click "New Appointment"
2. Select a service (Haircut, Beard, or Combo)
3. Choose a date
4. Wait for available slots to load
5. Select an available time slot
6. Add optional notes
7. Click "Create Appointment"

#### 4. View Your Appointments

- See all your appointments with status
- Cancel appointments if needed

#### 5. Cancel an Appointment

1. Find the appointment in your list
2. Click "Cancel" button
3. Confirm the cancellation

### For Administrators

#### 1. Login as Admin

1. Go to http://localhost:4200
2. Login with admin credentials:
   - Username: `barbershop_admin`
   - Password: `admin123`
3. You'll be redirected to `/appointments/today`

#### 2. View Today's Appointments

- See all appointments scheduled for today
- View client names and times
- Check appointment statuses

#### 3. Filter by Date

1. Use the date picker
2. Select any date
3. Click to load appointments for that date
4. Click "Show Today" to return to today's view

#### 4. View Client Details

1. Find an appointment
2. Click "Show Details"
3. View:
   - Client's full name
   - Email address
   - Phone number
   - Special notes

#### 5. Manage Appointments

**Confirm an Appointment:**
1. Click "Confirm" button
2. Status changes to "Confirmed" (green)

**Cancel an Appointment:**
1. Click "Cancel" button
2. Confirm the action
3. Status changes to "Canceled" (red)

#### 6. View All Appointments

- Click "View All" to see appointments from all dates
- Navigate to `/appointments` for complete list

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Authentication Endpoints

#### Register
```http
POST /auth/register/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123",
  "phone": "1234567890",
  "first_name": "John",
  "last_name": "Doe"
}

Response: 201 Created
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "role": "client",
  "phone": "1234567890",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### Login
```http
POST /auth/login/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securepass123"
}

Response: 200 OK
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Get Profile
```http
GET /auth/profile/
Authorization: Bearer {access_token}

Response: 200 OK
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "role": "client",
  "phone": "1234567890",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### Refresh Token
```http
POST /auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response: 200 OK
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Appointment Endpoints

#### Get Available Slots
```http
GET /appointments/available_slots/?date=2025-01-15
Authorization: Bearer {access_token}

Response: 200 OK
{
  "date": "2025-01-15",
  "available_slots": ["08:00", "09:00", "10:00", "14:00", "15:00"],
  "booked_slots": ["11:00", "12:00", "13:00"]
}
```

#### Create Appointment
```http
POST /appointments/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "service": "haircut",
  "appointment_date": "2025-01-15",
  "appointment_time": "10:00",
  "notes": "Short haircut please"
}

Response: 201 Created
{
  "id": 1,
  "service": "haircut",
  "appointment_date": "2025-01-15",
  "appointment_time": "10:00:00",
  "status": "pending",
  "notes": "Short haircut please"
}
```

#### Get My Appointments (Client)
```http
GET /appointments/my_appointments/
Authorization: Bearer {access_token}

Response: 200 OK
[
  {
    "id": 1,
    "client": 2,
    "client_details": {
      "id": 2,
      "username": "john_doe",
      "email": "john@example.com",
      "role": "client",
      "phone": "1234567890",
      "first_name": "John",
      "last_name": "Doe"
    },
    "service": "haircut",
    "appointment_date": "2025-01-15",
    "appointment_time": "10:00:00",
    "status": "pending",
    "notes": "Short haircut please",
    "created_at": "2025-01-12T10:30:00Z",
    "updated_at": "2025-01-12T10:30:00Z"
  }
]
```

#### Get Today's Appointments (Admin Only)
```http
GET /appointments/today/
Authorization: Bearer {admin_access_token}

Response: 200 OK
[
  {
    "id": 1,
    "client": 2,
    "client_details": {...},
    "service": "haircut",
    "appointment_date": "2025-01-13",
    "appointment_time": "10:00:00",
    "status": "pending",
    "notes": "Short haircut please",
    "created_at": "2025-01-12T10:30:00Z",
    "updated_at": "2025-01-12T10:30:00Z"
  }
]
```

#### Get Appointments by Date (Admin Only)
```http
GET /appointments/by_date/?date=2025-01-15
Authorization: Bearer {admin_access_token}

Response: 200 OK
[...]
```

#### Update Appointment Status
```http
PATCH /appointments/{id}/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "status": "confirmed"
}

Response: 200 OK
{
  "id": 1,
  "status": "confirmed",
  ...
}
```

#### Delete Appointment
```http
DELETE /appointments/{id}/
Authorization: Bearer {access_token}

Response: 204 No Content
```

### Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 204 | No Content - Successful deletion |
| 400 | Bad Request - Invalid data |
| 401 | Unauthorized - Invalid/missing token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

---

## 📁 Project Structure

```
rolosbarber/
│
├── backend/                          # Django Backend
│   ├── barbershop/                   # Main Django project
│   │   ├── __init__.py
│   │   ├── settings.py              # Django settings
│   │   ├── urls.py                  # Main URL configuration
│   │   ├── wsgi.py                  # WSGI config
│   │   └── asgi.py                  # ASGI config
│   │
│   ├── users/                        # Users app
│   │   ├── migrations/              # Database migrations
│   │   │   ├── __init__.py
│   │   │   └── 0001_initial.py
│   │   ├── __init__.py
│   │   ├── admin.py                 # Admin configuration
│   │   ├── apps.py                  # App configuration
│   │   ├── models.py                # User model with roles
│   │   ├── serializers.py           # DRF serializers
│   │   ├── views.py                 # Authentication views
│   │   ├── urls.py                  # Auth endpoints
│   │   └── tests.py                 # Unit tests
│   │
│   ├── appointments/                 # Appointments app
│   │   ├── migrations/              # Database migrations
│   │   │   ├── __init__.py
│   │   │   └── 0001_initial.py
│   │   ├── __init__.py
│   │   ├── admin.py                 # Admin configuration
│   │   ├── apps.py                  # App configuration
│   │   ├── models.py                # Appointment model
│   │   ├── serializers.py           # DRF serializers
│   │   ├── views.py                 # API views
│   │   ├── urls.py                  # Appointment endpoints
│   │   ├── permissions.py           # Custom permissions
│   │   └── tests.py                 # Unit tests
│   │
│   ├── manage.py                     # Django management script
│   ├── requirements.txt              # Python dependencies
│   ├── Dockerfile                    # Backend container config
│   ├── pytest.ini                    # Pytest configuration
│   └── .env.example                  # Environment variables template
│
├── frontend/                         # Angular Frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/          # Angular components
│   │   │   │   ├── login/
│   │   │   │   │   ├── login.component.ts
│   │   │   │   │   ├── login.component.html
│   │   │   │   │   └── login.component.css
│   │   │   │   ├── register/
│   │   │   │   ├── appointment-form/
│   │   │   │   ├── appointment-list/
│   │   │   │   └── admin-dashboard/
│   │   │   │
│   │   │   ├── services/            # Angular services
│   │   │   │   ├── auth.service.ts
│   │   │   │   └── appointment.service.ts
│   │   │   │
│   │   │   ├── guards/              # Route guards
│   │   │   │   └── auth.guard.ts
│   │   │   │
│   │   │   ├── interceptors/        # HTTP interceptors
│   │   │   │   └── auth.interceptor.ts
│   │   │   │
│   │   │   ├── models/              # TypeScript interfaces
│   │   │   │   └── models.ts
│   │   │   │
│   │   │   ├── app.component.ts     # Root component
│   │   │   └── app.routes.ts        # Route configuration
│   │   │
│   │   ├── environments/            # Environment configs
│   │   │   ├── environment.ts
│   │   │   └── environment.prod.ts
│   │   │
│   │   ├── index.html               # Main HTML
│   │   ├── main.ts                  # Bootstrap file
│   │   └── styles.css               # Global styles
│   │
│   ├── angular.json                  # Angular configuration
│   ├── package.json                  # Node dependencies
│   ├── tsconfig.json                 # TypeScript config
│   ├── Dockerfile                    # Frontend container config
│   └── nginx.conf                    # Nginx configuration
│
├── docker-compose.yml                # Docker orchestration
├── .gitignore                        # Git ignore rules
└── README.md                         # This file
```

---

## 🧪 Testing

### Backend Tests

Run all backend tests:

```bash
# Using pytest
docker exec -it barbershop_backend python manage.py test
```