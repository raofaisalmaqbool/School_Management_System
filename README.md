# School Management System

A comprehensive Django-based School Management System for managing students, teachers, courses, attendance, and leave applications.

## Features

### For Principal
- Dashboard with statistics (total students, teachers, courses)
- **Student Management**: Add, view, edit, and delete students
- **Teacher Management**: Add, view, edit, and delete teachers
- **Course Management**: Add, view, edit, and delete courses
- **Notifications**: Send notifications to teachers
- **Leave Management**: Approve or reject teacher and student leave applications

### For Teachers
- Dashboard with school statistics
- **Attendance Management**: Take and view attendance for courses
- **Notifications**: View notifications from principal
- **Leave Applications**: Apply for leave and view application history

### For Students
- Dashboard with school statistics
- **Leave Applications**: Apply for leave and view application status
- View enrolled courses and session information

## Technology Stack

- **Backend**: Django 3.2.9
- **Database**: MySQL / SQLite (configurable)
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Custom email-based authentication
- **Image Handling**: Pillow

## Project Structure

```
School_Management_System/
├── LMS/                          # Main application
│   ├── models.py                 # Database models
│   ├── admin.py                  # Admin configuration
│   ├── emailbackend.py           # Custom email authentication
│   ├── utils.py                  # Utility functions
│   ├── views/                    # View modules
│   │   ├── __init__.py
│   │   ├── auth_views.py         # Authentication views
│   │   ├── principal_views.py    # Principal-specific views
│   │   ├── teacher_views.py      # Teacher-specific views
│   │   └── student_views.py      # Student-specific views
│   └── migrations/               # Database migrations
├── School_Management_System/     # Project settings
│   ├── settings.py               # Configuration
│   ├── urls.py                   # URL routing
│   └── wsgi.py                   # WSGI configuration
├── static/                       # Static files (CSS, JS, images)
├── media/                        # User uploaded files
├── templates/                    # HTML templates
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables (local)
├── .env.example                  # Environment variables template
└── README.md                     # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- MySQL Server (optional, can use SQLite)

### Setup Instructions

1. **Clone the repository**
   ```bash
   cd /path/to/project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and configure your settings:
   ```env
   # Django Configuration
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # Database Configuration
   DB_ENGINE=sqlite  # or 'mysql'
   DB_NAME=db.sqlite3  # or your MySQL database name
   DB_USER=root
   DB_PASSWORD=your-password
   DB_HOST=localhost
   DB_PORT=3306
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Create static files directory**
   ```bash
   python manage.py collectstatic
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Open your browser and go to: `http://localhost:8000`
   - Admin panel: `http://localhost:8000/admin`

## Configuration

### Database Setup

#### Using SQLite (Default)
SQLite is configured by default. No additional setup required.

#### Using MySQL
1. Install MySQL server and create a database:
   ```sql
   CREATE DATABASE lms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. Update `.env` file:
   ```env
   DB_ENGINE=mysql
   DB_NAME=lms_db
   DB_USER=your_mysql_user
   DB_PASSWORD=your_mysql_password
   DB_HOST=localhost
   DB_PORT=3306
   ```

3. Install MySQL client:
   ```bash
   pip install mysqlclient
   ```

### Email Configuration (Optional)
To enable email notifications, update `.env`:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Usage

### Initial Setup

1. **Login to Admin Panel** (`/admin`)
   - Use the superuser credentials created earlier

2. **Create Session Years**
   - Add academic session years (e.g., "2023 To 2024")

3. **Create Courses**
   - Add courses/subjects

4. **Add Principal User**
   - Create a user with user_type='1'

5. **Add Teachers and Students**
   - Use the Principal dashboard to add teachers and students

### User Roles and Access

| Role      | User Type | Access                                      |
|-----------|-----------|---------------------------------------------|
| Principal | 1         | Full system access, manage all resources    |
| Teacher   | 2         | Take attendance, view notifications, apply leave |
| Student   | 3         | View dashboard, apply for leave             |

### Default Login
After creating users through the principal dashboard, they can login with:
- **Email**: The email address provided during registration
- **Password**: The password set during registration

## Models

### Core Models

- **Customuser**: Extended Django user model with role-based access
- **Teacher**: Teacher profile linked to Customuser
- **Student**: Student profile with course and session information
- **Course**: Subject/course information
- **Session_Year**: Academic year/session

### Operational Models

- **Attendance**: Daily attendance records per course
- **Attendance_Report**: Individual student attendance entries
- **Teacher_Notification**: Notifications sent to teachers
- **Teacher_leave**: Teacher leave applications
- **Student_Leave**: Student leave applications
- **Student_Result**: Student exam results and marks

## API Endpoints

### Authentication
- `GET /` - Login page
- `POST /doLogin/` - Authenticate user
- `GET /doLogout/` - Logout user
- `GET /profile/` - View user profile
- `POST /profile/update/` - Update user profile

### Principal URLs
- `GET /principal/home/` - Principal dashboard
- Student management: `/principal/student/[add|view|edit|delete]/`
- Teacher management: `/principal/teacher/[add|view|edit|delete]/`
- Course management: `/principal/course/[add|view|edit|delete]/`
- Leave management: `/principal/[teacher|student]/leave/[view|approve|reject]/`

### Teacher URLs
- `GET /teacher/home/` - Teacher dashboard
- `GET /teacher/notifications/` - View notifications
- Attendance: `/teacher/attendance/[take|save|view]/`
- Leave: `/teacher/leave/[apply|save]/`

### Student URLs
- `GET /student/home/` - Student dashboard
- Leave: `/student/leave/[apply|save]/`

## Development

### Running Tests
```bash
python manage.py test
```

### Creating New Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check your `.env` database credentials
   - Ensure MySQL server is running (if using MySQL)
   - Verify database exists

2. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check `STATIC_ROOT` and `STATICFILES_DIRS` in settings.py

3. **Image Upload Errors**
   - Ensure `media/` directory exists and is writable
   - Check `MEDIA_ROOT` and `MEDIA_URL` settings

4. **Login Issues**
   - Verify email and password are correct
   - Check that user's `user_type` is set correctly
   - Ensure user account is active

## Security Considerations

### Production Deployment

Before deploying to production:

1. **Change SECRET_KEY**
   - Generate a new secret key
   - Never commit `.env` to version control

2. **Set DEBUG=False**
   ```env
   DEBUG=False
   ```

3. **Configure ALLOWED_HOSTS**
   ```env
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

4. **Use HTTPS**
   - Enable SSL/TLS certificate
   - Set secure cookie flags

5. **Database Security**
   - Use strong database passwords
   - Limit database user permissions
   - Enable database encryption

6. **Regular Updates**
   - Keep Django and dependencies updated
   - Monitor security advisories

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For support, email: support@example.com

## Acknowledgments

- Django Framework
- Django Active Link
- All contributors and testers

## Version History

- **v1.0.0** (Current)
  - Initial release
  - Core functionality implemented
  - User management
  - Attendance system
  - Leave management
  - Notification system

## Future Enhancements

- [ ] Student result entry and report cards
- [ ] SMS notifications
- [ ] Email notifications for leave approvals
- [ ] Timetable management
- [ ] Fee management system
- [ ] Library management
- [ ] Examination module
- [ ] Parent portal
- [ ] Mobile app
- [ ] Analytics dashboard
- [ ] Export data to PDF/Excel
