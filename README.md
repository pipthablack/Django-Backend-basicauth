# Django JWT Authentication with Simple JWT

This project demonstrates how to implement JWT (JSON Web Tokens) authentication in a Django project using the `rest_framework_simplejwt` library.

## Installation

1. Install Django and Django REST framework:

```bash
pip install django djangorestframework
```

2. Install `rest_framework_simplejwt`:

```bash
pip install djangorestframework_simplejwt
```

3. Add the required apps to your `INSTALLED_APPS` in your Django project's settings.py file:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
]
```

4. Configure the authentication backend in your settings.py file:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
```

5. Add the JWT URLs to your project's urls.py file:

```python
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    ...
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

## Usage

1. Create a Django user using the `createsuperuser` command:

```bash
python manage.py createsuperuser
```

2. Start your Django development server:

```bash
python manage.py runserver
```

3. Use a tool like Postman or curl to obtain a JWT token by sending a POST request to `http://localhost:8000/api/token/` with the username and password of the created user.

4. Use the obtained access token in subsequent requests to your API by including it in the Authorization header with the format `Bearer <access_token>`.

## Additional Resources

- [Django REST framework Simple JWT documentation](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- [Django REST framework authentication](https://www.django-rest-framework.org/api-guide/authentication/)
- [JSON Web Tokens (JWT) RFC](https://tools.ietf.org/html/rfc7519)
