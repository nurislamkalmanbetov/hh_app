"""
Django settings for iwex_crm project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

import django.conf.locale
from django.conf import global_settings
from datetime import timedelta
import environ

from .juzmin import JAZZMIN_SETTINGS, JAZZMIN_UI_TWEAKS



env = environ.Env()
environ.Env.read_env(env_file='.env')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ADsafaegksdgfsdlgsklgk2444234dsflmfsdlgsdklgk34flskdgd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if not DEBUG:
    sentry_sdk.init(
        dsn="https://8fb81ab3c441492f88810ffd1b861a61@sentry.io/1806921",
        integrations=[DjangoIntegration()]
    )

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'smart_selects',
    'rangefilter',
    # 'applications.apps.SuitConfig',
    # 'applications.apps.JazzminConfig',

    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'schedule',
    'easy_thumbnails',
    'storages',
    'applications.accounts',
    'applications.core',
    'applications.bot',
    'applications.common',
    'drf_yasg2',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'corsheaders',
    'import_export',
    
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ]
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ROOT_URLCONF = 'iwex_crm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'iwex_crm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': 'iwex_new',
       'USER': 'postgres',
       'PASSWORD':  '123',
       'HOST': '127.0.0.1',
       'PORT':'5433',
   }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': env('POSTGRES_DB'),
#         'USER': env('POSTGRES_USER'),
#         'PASSWORD':  env('POSTGRES_PASSWORD'),
#         'HOST': env('POSTGRES_HOST'),
#         'PORT': env('POSTGRES_PORT'),
#     }
# }




# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

EXTRA_LANG_INFO = {
    'ky': {
        'bidi': False,  # right-to-left
        'code': 'ky',
        'name': 'Kyrgyz',
        'name_local': 'Кыргызча', #unicode codepoints here
    },
}

JQUERY_URL = True

LANG_INFO = dict(django.conf.locale.LANG_INFO.items())
LANG_INFO.update(EXTRA_LANG_INFO.items())
django.conf.locale.LANG_INFO = LANG_INFO

# Languages using BiDi (right-to-left) layout
global_settings.LANGUAGES.extend([('ky', 'Кыргызча'), ])

LANGUAGE_CODE = 'ru-ru'

LANGUAGES = (
    ('ru', 'Russian'),
    ('de', 'German'),
    ('en', 'English'),
    ('ky', 'Kyrgyz'),
)

LOCALE_PATHS = (
   os.path.join(BASE_DIR, 'locale'),
)


TIME_ZONE = 'Asia/Bishkek'


USE_I18N = True

USE_L10N = True

USE_TZ = True


# GMAIL SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = 'qvfflfeokayavhnp'
EMAIL_HOST_USER = 'kalmanbetovnurislam19@gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = 'IWEX'

default_app_config = 'applications.core.apps.CoreConfig'

# SENDGRID SMTP
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
# EMAIL_HOST_USER = env('EMAIL_HOST_USER')
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = 'IWEX'

AUTH_USER_MODEL = 'accounts.User'
JQUERY_URL = False

# Login url for @login_required decorator
LOGIN_URL = '/signin/'

CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Настройки для статических файлов
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Настройки для медиа-файлов
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

CORS_ORIGIN_ALLOW_ALL = True
IMPORT_EXPORT_USE_TRANSACTIONS = True


# settings.py
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = JAZZMIN_SETTINGS
JAZZMIN_UI_TWEAKS = JAZZMIN_UI_TWEAKS

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=60),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}
