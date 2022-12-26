"""
Django settings for ebdjango project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5=%aj2n#y80$(#k0*=s5hnlqob#sw&3#l4jv^0u5!nzr%syj#k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
STATIC_LOCAL = False
STRIPE_TEST = False

ALLOWED_HOSTS = ['casspea.herokuapp.com',
                 'www.casspea.co.uk',
                 'www2.casspea.co.uk',
                 'casspea2.herokuapp.com',
                 ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',
    'addresses',
    'boxes',
    'carts',
    'dashboards',
    'flavours',
    'orders',
    'lots',
    'store',
]

LOGIN_URL = '/login'
LOGIN_URL_REDIRECT = '/'
LOGOUT_URL = '/logout'
LOGOUT_REDIRECT_URL = '/login'

EMAIL_HOST = 'smtp-relay.sendinblue.com'
EMAIL_HOST_USER = 'casspea.sistemas@gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = 'IzGdtwJfFBNS7jXn'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'info@casspea.co.uk'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ebdjango.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'ebdjango.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

import dj_database_url

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
DATABASES['default']['CONN_MAX_AGE'] = 500

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

LOCAL_STATIC_CDN_PATH = os.path.join(os.path.dirname(BASE_DIR), 'static_cdn')

STATIC_ROOT = os.path.join(LOCAL_STATIC_CDN_PATH, 'static')  # live cdn AWS S3

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_ROOT = os.path.join(LOCAL_STATIC_CDN_PATH, 'media')
MEDIA_URL = '/media/'  # django-storages

AWS_ACCESS_KEY_ID = "AKIAIWMAKUKZAEUHDANQ"

AWS_SECRET_ACCESS_KEY = "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"

AWS_STORAGE_BUCKET_NAME = 'casspea-static-guork2'

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3-accelerate.amazonaws.com'

AWS_DEFAULT_ACL = 'public-read'

AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

AWS_LOCATION = 'static'

AWS_QUERYSTRING_AUTH = False

AWS_HEADERS = {'Access-Control-Allow-Origin': '*'}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'

EMAIL_STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}'

MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

AWS_S3_REGION_NAME = 'eu-west-2'
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# FORCE HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

STRIPE_PUBLIC_KEY = "pk_test_51MBMy0JiuFqKKcn6FsLlAE48ndzF9oruq219dkZArcnR6E0GN0Irv2X2ErvnPFbrgZyP1CP8Ay1hAdJNnnf7pa7Z00G3bxqyKY"
STRIPE_SECRET_KEY = "sk_test_51MBMy0JiuFqKKcn69O4Fc8Sz7UpmLoRoaxXbqxwO8CD20P2craNClm173MKMwO7ZyyvblMfifmupuPgrWKycMV7p00qiMAW9aX"
STRIPE_SECRET_KEY_LIVE = "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"
STRIPE_PUBLIC_KEY_LIVE = "pk_live_51MBMy0JiuFqKKcn6HYrAh3qBJz7x1Ajr5aqcKNzuKVQkr8xSYMdJVlQAV6uZ25HYRJ6kEsRyivTezDroICC3VeBq00q7edrNzB"
