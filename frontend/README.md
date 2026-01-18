# US-14: Django Website - Basic Setup 

## Structure
```
frontend/
├── manage.py              # Django management script
├── config/                # Django project settings
│   ├── settings.py       # Main configuration
│   ├── urls.py           # URL routing
│   ├── wsgi.py           # WSGI configuration
│   └── asgi.py           # ASGI configuration
├── core/                  # Main Django app
│   ├── models.py         # Database models (empty for now)
│   ├── views.py          # View functions
│   ├── urls.py           # App URL patterns
│   ├── admin.py          # Admin configuration
│   ├── templates/        # HTML templates
│   │   └── index.html    # Homepage
│   └── migrations/       # Database migrations
└── static/               # Static files (CSS, JS)
    ├── styles.css        # Stylesheet
    └── app.js            # JavaScript
```

## Running the Website

### Option 1: Using the batch file (from project root)
```bash
run_django.bat
```

### Option 2: Manual commands
```bash
cd frontend
python manage.py migrate
python manage.py runserver 8001
```
