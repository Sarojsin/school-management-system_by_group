# 🏫 School Management Portal

A comprehensive web-based school management system built with FastAPI, PostgreSQL, and Bootstrap. This portal provides separate dashboards for students, teachers, and school authorities with secure session management.

## ✨ Features

### 🎓 Student Dashboard
- View academic performance (marks, grades)
- Track attendance records
- Monitor assignments and due dates
- Access school notices and announcements
- Update personal profile information

### 👨‍🏫 Teacher Dashboard
- Add and manage student marks
- Record attendance for classes
- Create and assign homework/assignments
- View all students and their performance
- Track teaching activities

### 🏛️ Authority Dashboard
- Manage school notices and announcements
- Set and update fee structures
- Oversee students and teachers
- Administrative controls and statistics
- System-wide management tools

### 🔐 Security Features
- Secure session-based authentication
- Role-based access control
- Password hashing with bcrypt
- Protected routes and data isolation

## 🗄️ Database Architecture

The system uses **4 separate PostgreSQL databases** for data isolation and security:

1. **school_public** - User authentication and basic profiles
2. **school_students** - Student data, marks, attendance, assignments
3. **school_teachers** - Teacher profiles and subject assignments
4. **school_authority** - Notices, fee structures, administrative data

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Git

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd school_dashboard_project
```

2. **Set up PostgreSQL databases**
```bash
# Update credentials in setup_databases.py if needed
python setup_databases.py
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure database connections**
Edit `app/config.py` and update database URLs:
```python
DATABASE_CONFIGS = {
    "student": "postgresql://username:password@localhost:5432/school_students",
    "teacher": "postgresql://username:password@localhost:5432/school_teachers", 
    "authority": "postgresql://username:password@localhost:5432/school_authority",
    "public": "postgresql://username:password@localhost:5432/school_public"
}
```

5. **Run the application**
```bash
cd app
python main.py
```

6. **Access the portal**
Open your browser and navigate to: `http://localhost:8000`

## 🔑 Demo Credentials

| Role | Username | Password |
|------|----------|----------|
| Student | student1 | password123 |
| Teacher | teacher1 | password123 |
| Authority | admin1 | password123 |

## 📁 Project Structure

```
school_dashboard_project/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py              # Database and app configuration
│   ├── database.py            # Database connections and sessions
│   ├── models.py              # SQLAlchemy ORM models
│   ├── tables.py              # Pydantic schemas
│   ├── repositories/          # Data access layer
│   │   ├── user_repository.py
│   │   └── student_repository.py
│   ├── routes/                # API routes and web handlers
│   │   ├── auth.py           # Authentication routes
│   │   ├── students.py       # Student dashboard routes
│   │   ├── teacher.py        # Teacher dashboard routes
│   │   └── authority.py      # Authority dashboard routes
│   ├── templates/            # Jinja2 HTML templates
│   │   ├── base.html         # Base template
│   │   ├── index.html        # Landing page
│   │   ├── login.html        # Login form
│   │   ├── signup.html       # Registration form
│   │   ├── student_dashboard.html
│   │   ├── teacher_dashboard.html
│   │   └── authority_dashboard.html
│   └── static/              # CSS, JS, and assets
│       ├── css/style.css    # Custom styles
│       └── js/script.js     # Interactive features
├── requirements.txt         # Python dependencies
├── setup_databases.py      # Database setup script
└── README.md               # This file
```

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python web framework)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Templates**: Jinja2
- **Authentication**: Session-based with secure cookies
- **Security**: bcrypt password hashing, CSRF protection

## 🎯 Key Features Explained

### Multi-Database Architecture
Each role has its dedicated database ensuring:
- **Data Isolation**: Students can't access teacher data
- **Security**: Compromised credentials limit damage scope
- **Scalability**: Individual database optimization
- **Compliance**: Easier to manage data privacy regulations

### Session Management
- Secure session cookies with proper expiration
- Role-based route protection
- Automatic logout on session expiry
- CSRF protection on forms

### Real-time Dashboard Features
- Live performance tracking for students
- Interactive grade calculation for teachers
- Dynamic notice management for authorities
- Responsive design for all devices

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-super-secret-key-change-this-in-production
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
```

### Security Settings
Update `app/config.py` for production:
```python
SECRET_KEY = "change-this-in-production"
DEBUG = False  # Set to False in production
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

## 📝 API Endpoints

### Authentication
- `GET /` - Landing page
- `GET /login` - Login form
- `POST /login` - Process login
- `GET /signup` - Registration form
- `POST /signup` - Process registration
- `GET /logout` - Logout user

### Student Routes
- `GET /student/dashboard` - Student dashboard
- `GET /student/profile` - Student profile
- `POST /student/profile/update` - Update profile

### Teacher Routes
- `GET /teacher/dashboard` - Teacher dashboard
- `GET /teacher/students` - View all students
- `GET /teacher/add-marks` - Add marks form
- `POST /teacher/add-marks` - Process marks
- `GET /teacher/add-attendance` - Attendance form
- `POST /teacher/add-attendance` - Process attendance

### Authority Routes
- `GET /authority/dashboard` - Authority dashboard
- `GET /authority/notices` - Manage notices
- `GET /authority/add-notice` - Add notice form
- `POST /authority/add-notice` - Process notice
- `GET /authority/fee-structure` - Manage fees

## 🚀 Deployment

### Production Checklist
- [ ] Update `SECRET_KEY` in config
- [ ] Set `DEBUG = False`
- [ ] Use environment variables for database credentials
- [ ] Set up proper PostgreSQL user permissions
- [ ] Configure reverse proxy (nginx/Apache)
- [ ] Set up SSL certificates
- [ ] Configure backup strategy
- [ ] Set up monitoring and logging

### Docker Deployment (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "app/main.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

Copyright (c) 2023 SAROJ SINGH DHAMI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 🆘 Troubleshooting

### Common Issues

**Database Connection Error**
- Ensure PostgreSQL is running
- Check database credentials in `config.py`
- Verify database names exist

**Import Errors**
- Run `pip install -r requirements.txt`
- Check Python version (3.8+ required)

**Template Not Found**
- Ensure you're running from the `app/` directory
- Check template paths in routes

**Session Issues**
- Clear browser cookies
- Check `SECRET_KEY` configuration
- Restart the application

### Getting Help

- Check the [Issues](../../issues) page
- Create a new issue with detailed error logs
- Include your Python and PostgreSQL versions

## 🎉 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- UI components from [Bootstrap](https://getbootstrap.com/)
- Icons by [Font Awesome](https://fontawesome.com/)
- Database management with [SQLAlchemy](https://sqlalchemy.org/)

---

Made with ❤️ for educational institutions worldwide
created my 
1.saroj singh dhami
2.
3.
