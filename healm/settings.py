"""
Django settings for healm project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from django.core.management.utils import get_random_secret_key
from pathlib import Path
import os
import sys
import dj_database_url


#| #### Comment/Uncomment These For Local Environment ####
#|
#V
# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = os.getenv("DEBUG", "False") == "True"  # Comment out for local enviornment
DEBUG = True # Uncomment for local enviornment

#DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True" # Comment out for local enviornment
DEVELOPMENT_MODE = True # Uncomment for local environment
#^
#|
#| #### Comment/Uncomment These For Local Environment ####

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'frontpage',
    'django.contrib.sites',
    #'rest_framework',
    #'rest_framework.authtoken',
    #'rest_auth',
    'allauth',
    'allauth.account',
    #'rest_auth.registration',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'healm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR /'templates'],
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

WSGI_APPLICATION = 'healm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

if DEVELOPMENT_MODE is True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if os.getenv("DATABASE_URL", None) is None:
        raise Exception("DATABASE_URL environment variable not defined")
    DATABASES = {
        "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),
    }

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontpage/templates/'),
]
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online'
        }, 
        'APP': {
            'client_id': '521282700960-lju3vq4krsln6o5et598s1sk0v2d42le.apps.googleusercontent.com',
            'secret': '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',
            'key':''
        }
    }
}

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'info',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

ADMINS = [('healmteam', 'healmteam@protonmail.com')]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'healmteam@gmail.com'
EMAIL_HOST_PASSWORD = 'b00@UV$wCOAJeZgW'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters':{
        'simple': {
            'format': '[{levelname}] [{asctime}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'error.log',
            'formatter':'simple',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level' : 'INFO',
            'formatter':'simple',
        },
        'mail_admins': {
            'level': 'CRITICAL',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter':'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


