# IMCreate

## About
An image hosting social media-like website.

## Getting Started
Necessary packages:
- `django-taggit`
- `django-resized`
```
pip install django-taggit django-resized
```

How to run:
```
python manage.py migrate
python manage.py runserver [IP address:Port]
```

When editing:
```
python manage.py makemigrations comments/posts/social/users
python manage.py migrate
```