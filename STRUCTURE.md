# Project Structure

This document describes the organization and structure of the School Management System project.

## Directory Tree

```
School_Management_System/
├── .github/                      # GitHub configuration
├── LMS/                          # Main Django application
│   ├── __init__.py
│   ├── admin.py                  # Django admin configuration
│   ├── apps.py                   # App configuration
│   ├── emailbackend.py           # Custom email authentication backend
│   ├── forms.py                  # Django forms for all models
│   ├── models.py                 # Database models
│   ├── tests.py                  # Unit tests
│   ├── utils.py                  # Utility functions and validators
│   ├── migrations/               # Database migration files
│   │   └── __init__.py
│   └── views/                    # View modules (organized by user type)
│       ├── __init__.py           # Package initialization
│       ├── auth_views.py         # Authentication and profile views
│       ├── principal_views.py    # Principal-specific views
│       ├── teacher_views.py      # Teacher-specific views
│       └── student_views.py      # Student-specific views
│
├── School_Management_System/     # Django project settings
│   ├── __init__.py
│   ├── asgi.py                   # ASGI configuration
│   ├── settings.py               # Project settings (with env vars)
│   ├── urls.py                   # Main URL routing
│   └── wsgi.py                   # WSGI configuration
│
├── static/                       # Static files (CSS, JS, Images)
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                        # User uploaded files
│   └── profile_pics/             # Profile pictures
│
├── templates/                    # HTML templates
│   ├── base.html                 # Base template
│   ├── index.html                # Home page
│   ├── login.html                # Login page
│   ├── profile.html              # User profile page
│   ├── principal/                # Principal templates
│   │   ├── principal_home.html
│   │   ├── add_student.html
│   │   ├── view_student.html
│   │   ├── edit_student.html
│   │   ├── add_teacher.html
│   │   ├── view_teacher.html
│   │   ├── edit_teacher.html
│   │   ├── add_course.html
│   │   ├── view_course.html
│   │   ├── edit_course.html
│   │   ├── teacher_notification.html
│   │   ├── teacher_leave.html
│   │   └── student_leave.html
│   ├── teacher/                  # Teacher templates
│   │   ├── teacher_home.html
│   │   ├── teacher_notification.html
│   │   ├── teacher_leave_apply.html
│   │   ├── take_attendance.html
│   │   └── view_attendance.html
│   └── student/                  # Student templates
│       ├── student_home.html
│       └── student_leave_apply.html
│
├── .env                          # Environment variables (not in git)
├── .env.example                  # Example environment variables
├── .gitignore                    # Git ignore rules
├── CHANGELOG.md                  # Project changelog
├── CONTRIBUTING.md               # Contribution guidelines
├── LICENSE                       # MIT License
├── README.md                     # Main documentation
├── STRUCTURE.md                  # This file
├── db.sqlite3                    # SQLite database (if using SQLite)
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
└── setup.sh                      # Setup automation script
```

## Application Architecture

### Models Layer (`LMS/models.py`)

The data layer consisting of Django ORM models:

- **Customuser**: Extended User model with role-based access (Principal/Teacher/Student)
- **Teacher**: Teacher profile with address and contact info
- **Student**: Student profile linked to courses and sessions
- **Course**: Subjects/courses taught in the school
- **Session_Year**: Academic years/sessions
- **Attendance**: Daily attendance records per course
- **Attendance_Report**: Individual student attendance entries
- **Teacher_Notification**: Notifications sent to teachers
- **Teacher_leave**: Teacher leave applications
- **Student_Leave**: Student leave applications
- **Student_Result**: Student exam results and grades

### Views Layer (`LMS/views/`)

Organized by user role for better maintainability:

#### Auth Views (`auth_views.py`)
- `login()` - Display login page
- `doLogin()` - Authenticate and redirect users
- `doLogout()` - Logout user
- `profile()` - Display user profile
- `profile_update()` - Update user profile
- `index()` - Home page
- `base()` - Base template (for testing)

#### Principal Views (`principal_views.py`)
- **Dashboard**: `principal_home()`
- **Student Management**: `add_student()`, `view_student()`, `edit_student()`, `update_student()`, `delete_student()`
- **Teacher Management**: `add_teacher()`, `view_teacher()`, `edit_teacher()`, `delete_teacher()`
- **Course Management**: `add_course()`, `view_course()`, `edit_course()`, `update_course()`, `delete_course()`
- **Notifications**: `teacher_send_notification()`, `save_teacher_notification()`
- **Leave Management**: `teacher_leave_view()`, `teacher_leave_approve()`, `teacher_leave_disapprove()`
- **Student Leave**: `student_leave_view()`, `student_leave_approve()`, `student_leave_disapprove()`

#### Teacher Views (`teacher_views.py`)
- **Dashboard**: `teacher_home()`
- **Notifications**: `notifications_teacher()`, `status_mark()`
- **Leave**: `teacher_leave_apply()`, `teacher_leave_save()`
- **Attendance**: `teacher_take_attendance()`, `teacher_save_attendance()`, `teacher_view_attendance()`

#### Student Views (`student_views.py`)
- **Dashboard**: `student_home()`
- **Leave**: `student_apply_leave()`, `student_save_leave()`

### URL Configuration (`School_Management_System/urls.py`)

RESTful URL patterns organized by functionality:

```
/                                  # Login page
/doLogin/                          # Login action
/doLogout/                         # Logout action
/profile/                          # User profile
/profile/update/                   # Update profile

/principal/home/                   # Principal dashboard
/principal/student/[action]/       # Student management
/principal/teacher/[action]/       # Teacher management
/principal/course/[action]/        # Course management

/teacher/home/                     # Teacher dashboard
/teacher/notifications/            # View notifications
/teacher/leave/[action]/           # Leave management
/teacher/attendance/[action]/      # Attendance management

/student/home/                     # Student dashboard
/student/leave/[action]/           # Leave management
```

### Forms Layer (`LMS/forms.py`)

Django forms for data validation and rendering:

- `CustomUserCreationForm` - User registration
- `CustomUserChangeForm` - User profile updates
- `StudentForm` - Student data entry
- `TeacherForm` - Teacher data entry
- `CourseForm` - Course creation/editing

### Utilities (`LMS/utils.py`)

Helper functions and validators:

- `FormValidator` - Class with validation methods
  - `validate_name()` - Name validation
  - `validate_email()` - Email format validation
  - `validate_username()` - Username validation
  - `validate_password()` - Password strength check
  - `validate_image()` - Image file validation
  - `validate_required_fields()` - Required field checker

- `get_status_display()` - Convert status code to text
- `get_user_type_display()` - Convert user type to text

### Admin Interface (`LMS/admin.py`)

Enhanced Django admin with:
- Custom list displays for all models
- Search and filter capabilities
- Inline editing where appropriate
- Custom methods for computed fields
- Improved user experience

## Data Flow

### Authentication Flow
```
User enters credentials → EmailBackend.authenticate()
→ Check credentials → Create session
→ Redirect based on user_type (Principal/Teacher/Student)
```

### Request Flow
```
URL Request → urls.py → View Function
→ Check authentication/permissions
→ Process data/Query database
→ Render template with context
→ Return HTTP Response
```

### Form Submission Flow
```
User submits form → POST request → View function
→ Validate input data
→ Check business logic
→ Save to database (with try-except)
→ Display success/error message
→ Redirect to appropriate page
```

## Configuration Files

### `.env`
Environment-specific configuration:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `ALLOWED_HOSTS` - Comma-separated hostnames
- `DB_ENGINE` - Database type (sqlite/mysql)
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` - Database credentials
- `STATIC_URL`, `MEDIA_URL` - File serving paths

### `settings.py`
Main Django configuration using environment variables:
- Database configuration
- Installed apps
- Middleware
- Template settings
- Static/Media file configuration
- Authentication backends

### `requirements.txt`
Python package dependencies:
- Django 3.2.9
- mysqlclient
- Pillow
- django-active-link
- python-decouple

## Security Considerations

### Implemented Security Features
1. **Environment Variables**: Sensitive data in `.env` file
2. **CSRF Protection**: Django's built-in CSRF middleware
3. **Password Hashing**: Django's password hashing
4. **SQL Injection Protection**: Django ORM
5. **XSS Protection**: Django template auto-escaping
6. **Authentication**: Custom email-based authentication
7. **Authorization**: Login required decorators

### Security Best Practices
- Never commit `.env` to version control
- Use strong `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Configure proper `ALLOWED_HOSTS`
- Use HTTPS in production
- Regular dependency updates
- Input validation on all forms
- Proper error handling

## Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/feature-name
   ```

2. **Make Changes**
   - Write code following PEP 8
   - Add docstrings
   - Include error handling

3. **Test Changes**
   ```bash
   python manage.py test
   ```

4. **Run Migrations** (if models changed)
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Commit Changes**
   ```bash
   git commit -m "feat: add feature description"
   ```

6. **Push and Create PR**
   ```bash
   git push origin feature/feature-name
   ```

## Deployment Structure

For production deployment:

```
/var/www/school_management/
├── venv/                  # Virtual environment
├── School_Management_System/  # Project code
├── logs/                  # Application logs
├── backups/              # Database backups
└── ssl/                  # SSL certificates
```

## Database Schema

See models.py for complete schema. Key relationships:

```
Customuser (1) ←→ (1) Teacher
Customuser (1) ←→ (1) Student
Teacher (1) ←→ (n) Course
Course (1) ←→ (n) Student
Session_Year (1) ←→ (n) Student
Course (1) ←→ (n) Attendance
Attendance (1) ←→ (n) Attendance_Report
Student (1) ←→ (n) Attendance_Report
```

## Performance Considerations

- **Query Optimization**: Use `select_related()` for foreign keys
- **Indexing**: Database indexes on frequently queried fields
- **Caching**: Consider Django's caching framework for production
- **Static Files**: Serve static files through CDN in production
- **Database**: Use PostgreSQL for production (better performance than SQLite)

## Future Enhancements

See CHANGELOG.md for the complete roadmap.

## Support

For questions about the project structure, see:
- README.md - General documentation
- CONTRIBUTING.md - Contribution guidelines
- CHANGELOG.md - Version history and changes
