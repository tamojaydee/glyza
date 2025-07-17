# Pancake Cinema Workflows

## Overview

Pancake Cinema Workflows is a Flask-based web application that provides a fun, cinema-themed task management system. The application allows users to create accounts, manage tasks with different statuses (pending, in-progress, done), and track their workflow progress through an intuitive dashboard interface.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy extension
- **Architecture Pattern**: Modular blueprint-based structure
- **Session Management**: Flask sessions for user authentication
- **Security**: Werkzeug password hashing and ProxyFix middleware

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default)
- **CSS Framework**: Bootstrap 5.3.0
- **Icons**: Font Awesome 6.4.0
- **Fonts**: Google Fonts (Fredoka One for titles, Nunito for body text)
- **Theme**: Custom "Cinema-Pancake" theme with yellow/golden color scheme

### Database Design
- **Primary Database**: SQLite (development) with PostgreSQL support via DATABASE_URL
- **ORM**: SQLAlchemy with DeclarativeBase
- **Connection Pooling**: Configured with pool_recycle and pool_pre_ping

## Key Components

### Models (models.py)
- **User Model**: Handles user authentication, profile management, and relationships
  - Fields: id, username, email, password_hash, name, avatar_url, bio, created_at
  - Methods: set_password(), check_password(), get_avatar_url()
  - Relationship: One-to-many with tasks

- **Task Model**: Manages workflow tasks
  - Fields: id, title, description, status, priority, due_date, created_at, updated_at, user_id
  - Status options: pending, in-progress, done
  - Priority levels: low, medium, high

### Route Blueprints
- **Auth Blueprint** (/auth): Handles login and registration
- **Workflow Blueprint** (/workflow): Manages dashboard and task operations
- **Profile Blueprint** (/profile): User profile viewing and editing

### Authentication System
- Session-based authentication using Flask sessions
- Password hashing with Werkzeug security functions
- Login required decorator for protected routes
- User session management with user_id and username storage

## Data Flow

1. **User Registration/Login**: 
   - User submits credentials → Auth blueprint validates → Session created → Redirect to dashboard

2. **Task Management**:
   - Dashboard loads user's tasks with filtering/search → Task CRUD operations → Database updates → Real-time dashboard refresh

3. **Profile Management**:
   - User views profile → Edit form submission → Validation → Database update → Profile refresh

## External Dependencies

### Python Packages
- Flask: Web framework
- Flask-SQLAlchemy: Database ORM
- Werkzeug: WSGI utilities and security functions

### Frontend Dependencies (CDN)
- Bootstrap 5.3.0: UI framework
- Font Awesome 6.4.0: Icon library
- Google Fonts: Typography (Fredoka One, Nunito)

### Development Dependencies
- Python logging: Application logging and debugging

## Deployment Strategy

### Environment Configuration
- **Session Secret**: Configurable via SESSION_SECRET environment variable
- **Database URL**: Configurable via DATABASE_URL (defaults to SQLite)
- **Proxy Support**: ProxyFix middleware for deployment behind reverse proxies

### Database Strategy
- **Development**: SQLite with automatic table creation
- **Production**: PostgreSQL support via DATABASE_URL
- **Migration**: SQLAlchemy create_all() for automatic schema deployment

### Server Configuration
- **WSGI Application**: Standard Flask WSGI app
- **Host/Port**: Configurable (defaults to 0.0.0.0:5000)
- **Debug Mode**: Enabled for development

### Static Assets
- CSS: Custom cinema-pancake theme with CSS variables
- JavaScript: Enhanced UX with Bootstrap integration and animations
- Images: Pancake icon and avatar system

The application is designed to be easily deployable on platforms like Replit, Heroku, or any WSGI-compatible hosting service with minimal configuration changes.