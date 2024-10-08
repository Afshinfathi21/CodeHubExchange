"""
Django settings for uut_forum_webapi project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
AUTH_USER_MODEL='accounts.CustomUser'

CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False')

ALLOWED_HOSTS = ['*']
CRISPY_TEMPLATE_PACK = 'bootstrap4'


# Emailing settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.codehubexchange.ir'  # Use your cPanel mail server hostname  
EMAIL_HOST_USER = 'support@codehubexchange.ir'  # Use your email address
EMAIL_FROM = 'support@codehubexchange.ir'
EMAIL_HOST_PASSWORD = 'gz4b{qxL{[%B'  # Use your email password
EMAIL_PORT = 567  # Use the appropriate port for your cPanel mail server
EMAIL_USE_TLS = True
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'accounts',
    'tags',
    'discutions',
    'questions',
    'rest_framework',
    'crispy_forms',
    "crispy_bootstrap4",
    'ckeditor',
    'ckeditor_uploader',
    'knox',
    'tagify'
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.middleware.TokenMiddleware',
    'accounts.middleware.AdminAccessMiddleware',
]

ROOT_URLCONF = 'uut_forum_webapi.urls'

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

WSGI_APPLICATION = 'uut_forum_webapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "CodeHubExchange",
#         "USER": "postgres",
#         "PASSWORD": "",
#         "HOST": "localhost",
#         "PORT": "5433",
#     }
# }


CKEDITOR_CONFIGS = {
    'awesome_ckeditor': {
        'toolbar': 'Basic',
    },
}

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono-lisa',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike',]},
            {'name': 'paragraph',
             'items': [
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'BidiLtr', 'BidiRtl']},
            {'name': 'insert',
             'items': ['Image','Smiley','CodeSnippet']},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        # 'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath',
            'codesnippet'
        ]),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT=BASE_DIR / "static"


MEDIA_ROOT=BASE_DIR /'media'
MEDIA_URL='/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Set session timeout to 15 minutes (900 seconds)
SESSION_COOKIE_AGE = 900
# SESSION_COOKIE_SECURE = True
# APPEND_SLASH = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
SESSION_SAVE_EVERY_REQUEST = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication',),
    'EXCEPTION_HANDLER': 'accounts.exceptions.custom_exception_handler',
}

from datetime import timedelta
from rest_framework.settings import api_settings

REST_KNOX = {
  'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
  'AUTH_TOKEN_CHARACTER_LENGTH': 64,
  'TOKEN_TTL': timedelta(days=2),
  'TOKEN_LIMIT_PER_USER': None,
  'AUTO_REFRESH': False,
}
