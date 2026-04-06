import os
from pathlib import Path
import pymysql

# 1. Tell Django to use pymysql instead of mysqlclient
pymysql.version_info = (2, 2, 1, 'final', 0)
pymysql.install_as_MySQLdb()

# 2. Trick Django into thinking MariaDB is version 10.6.0
import django
from django.db.backends.mysql.base import DatabaseWrapper
DatabaseWrapper.server_version = (10, 6, 0)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-local-dev-key-do-not-use-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Your Custom App
    'complaints',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'complaint_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'complaint_system.wsgi.application'

# Database
# Using SQLite for local development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'

# Indian Standard Time for accurate complaint timestamps
TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

<<<<<<< HEAD
# This ignores the version check error
SILENCED_SYSTEM_CHECKS = ["mysql.W002"]

# settings.py

# Tells Django where to redirect unauthenticated users
LOGIN_URL = 'login'

# Tells Django where to redirect users after they successfully log in
LOGIN_REDIRECT_URL = 'dashboard'
<<<<<<< HEAD

# Ignores the MySQL version check warning
SILENCED_SYSTEM_CHECKS = ["mysql.W002"]
=======
=======
>>>>>>> f5ebbec0d959c11e1eb788da489f5874fb3afbd5
# Media files configuration (Uploaded images)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
>>>>>>> 158c7d539b93e69ab1ceb38b4bd0005e0b5c0f17
