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
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5=%aj2n#y80$(#k0*=s5hnlqob#sw&3#l4jv^0u5!nzr%syj#k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
STATIC_LOCAL = True
STRIPE_TEST = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'accounts',
    'addresses',
    'boxes',
    'carts',
    'custom_boxes',
    'custom_chocolates',
    'dashboards',
    'discounts',
    'flavours',
    'orders',
    'lots',
    'store',
    'shipping',
    'leads',
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
CONTACT_EMAIL = 'carlosblancosierra@gmail.com'
STAFF_EMAILS = ['carlosblancosierra@gmail.com']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ebdjango.middleware.utm_middleware.UTMMiddleware',
    'ebdjango.middleware.visited_pages_middleware.VisitedPagesMiddleware',
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
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STRIPE_PUBLIC_KEY = "pk_test_51MBMy0JiuFqKKcn6FsLlAE48ndzF9oruq219dkZArcnR6E0GN0Irv2X2ErvnPFbrgZyP1CP8Ay1hAdJNnnf7pa7Z00G3bxqyKY"
STRIPE_SECRET_KEY = "sk_test_51MBMy0JiuFqKKcn69O4Fc8Sz7UpmLoRoaxXbqxwO8CD20P2craNClm173MKMwO7ZyyvblMfifmupuPgrWKycMV7p00qiMAW9aX"

# MESSAGE BOOTSTRAP
MESSAGE_TAGS = {
    messages.ERROR: 'red',
    messages.SUCCESS: 'green',
}

UTMMIDDLEWARE_INCLUDE_PARAMETERS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'utm_id']
UTMMIDDLEWARE_SESSION_EXPIRY = 24 * 60 * 60  # Default to 24 hours
