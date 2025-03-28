"""
Django settings for proiect1 project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9$uiy8j_x94_w_nj*y(*zifq^*)56)pcno5vuxd+y3_n!@m%9b'

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
    'aplicatie_ex.apps.AplicatieExConfig',
    'django.contrib.auth.management.commands',
    'django.core.management',
    'django.contrib.sites',
    'django.contrib.sitemaps',
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend'
    # 'backend.personalizat'
]

# laborator7
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587 
EMAIL_USE_TLS = True 
EMAIL_HOST_USER = 'flavorcalifornia@gmail.com'
EMAIL_HOST_PASSWORD = 'bcxzcnwpmmbsjmmz'
DEFAULT_FROM_EMAIL = 'Your favorite coffee shop <flavorcalifornia@gmail.com>'

ADMINS = [
    ('Admin1', 'flavorcalifornia@gmail.com'),
    ('Admin2', 'nichitaiulia48@gmail.com'),
]


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {message}',
#             'style': '{',
#         },
#         'simple': {
#             'format': '{levelname} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'WARNING',
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple',
#         },
#         'file_debug': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': 'debug.log',
#             'formatter': 'verbose',
#         },
#         'file_info': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': 'info.log',
#             'formatter': 'verbose',
#         },
#         'file_warning': {
#             'level': 'WARNING',
#             'class': 'logging.FileHandler',
#             'filename': 'warning.log',
#             'formatter': 'verbose',
#         },
#         'file_error': {
#             'level': 'ERROR',
#             'class': 'logging.FileHandler',
#             'filename': 'error.log',
#             'formatter': 'verbose',
#         },
#         'file_critical': {
#             'level': 'CRITICAL',
#             'class': 'logging.FileHandler',
#             'filename': 'critical.log',
#             'formatter': 'verbose',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console', 'file_debug', 'file_info', 'file_warning', 'file_error', 'file_critical'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'proiect1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'aplicatie_ex/templates')],
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

WSGI_APPLICATION = 'proiect1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
                'options': '-c search_path=django'
        },
        'NAME': 'cafenea',
        'USER': 'iulia',
        'PASSWORD': '6545',
        'HOST': 'localhost',  # sau IP-ul serverului
        'PORT': '5432',       # portul implicit pentru PostgreSQL
    }

}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

# laborator6
AUTH_USER_MODEL = 'aplicatie_ex.CustomUser'

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
# Dacă fișierele statice sunt organizate pe aplicații, setările pot arăta astfel:
STATICFILES_DIRS = [
    BASE_DIR / 'aplicatie_ex/static',  # Locația fișierelor statice din aplicație
]

MEDIA_ROOT ='/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# laborator9
from django.contrib.messages import constants as message_constants

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

#Personalizarea nivelurilor de mesaje:
MESSAGE_TAGS = {
    message_constants.DEBUG: 'debug',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'error',
}


