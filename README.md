# IMCreate

## About
An image hosting social media-like website.

## Getting Started
Necessary packages:
```
pip install -r requirements.txt
```

How to run:
```
python manage.py migrate
python manage.py runserver [IP address:Port]
```

When editing app models:
```
python manage.py makemigrations [comments/posts/social/users]
python manage.py migrate
```
