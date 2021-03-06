"""
Django settings for care project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import re
import logging

# This imports ENV from our .env file./Shell Environment
from .dotenv import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = <Imported via .env>

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = <Imported via .env>

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'taggit',
    'care.data',
    'care.frontend',
    'care.sms',
    'care.survey',
    'rest_framework'
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

ROOT_URLCONF = 'care.urls'

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

WSGI_APPLICATION = 'care.wsgi.application'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# File storage paths
# PROTECTED_PATH & PROTECTED_ROOT import from .env
if(not ENV_IMPORTED):
    # Need a sane default
    PROTECTED_PATH = 'protected'
    PROTECTED_ROOT = os.path.join('/tmp', PROTECTED_PATH)

PROTECTED_URL = f'/{PROTECTED_PATH}/'
PROTECTED_PATH = PROTECTED_URL.strip('/')
BATCH_PATH = 'media/batch'
BATCH_MEDIA_URL = os.path.join(PROTECTED_URL, BATCH_PATH, '')

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
if(ENV_IMPORTED):
    ## Don't be fooled, this only works with .env!!
    DATABASES = {
        "default": {
            # Add "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            # DB name or path to database file if using sqlite3.
            "NAME": DJANGO_DB_NAME,
            # Not used with sqlite3.
            "USER": DJANGO_DB_USER,
            # Not used with sqlite3.
            "PASSWORD": DJANGO_DB_PASS,
            # Set to empty string for localhost. Not used with sqlite3.
            "HOST": DJANGO_DB_HOST,
            # Set to empty string for default. Not used with sqlite3.
            "PORT": DJANGO_DB_PORT,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Phoenix'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

###########
# LOGGING #
###########

### DON'T BE FOOLED: This logging only works with .env active!!
if(ENV_IMPORTED):
    if(SENTRY_DSN_URL):
        try:
            import sentry_sdk
            from sentry_sdk.integrations.django import DjangoIntegration
            from sentry_sdk.integrations.logging import LoggingIntegration
        except ImportError:
            pass
        else:
            sentry_logging = LoggingIntegration(
                level=logging.INFO,  # might be too agressive?
                event_level=logging.ERROR,
            )
            sentry_sdk.init(
                dsn=SENTRY_DSN_URL,
                integrations=[sentry_logging, DjangoIntegration(), ],
                # If you wish to associate users to errors (assuming you are using
                # django.contrib.auth) you may enable sending PII data.
                send_default_pii=True
            )

    if(sys.platform == 'darwin'):
        syslog_address = '/var/run/syslog'
    elif(re.match('^freebsd.*', sys.platform)):
        syslog_address = '/var/run/log'
    else:
        syslog_address = '/dev/log'

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            }
        },
        'root': {
            'handlers': ['console', 'mail_admins'],
            'level': ROOT_LOG_LEVEL,
        },
        'handlers': {
            # 'syslog': {
            #     'level': 'INFO',
            #     'class': 'logging.handlers.SysLogHandler',
            #     'filters': ['require_debug_false', ],
            #     'address': syslog_address,
            #     'formatter': 'detailed',
            # },
            'console': {
                'class': 'logging.StreamHandler',
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'filters': ['require_debug_false', ],
                'include_html': True,
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'mail_admins'],
                'level': DJANGO_LOG_LEVEL,
                'propagate': True,
            },
            'django.request': {
                # 'handlers': ['mail_admins', 'console', 'sentry', ],
                'handlers': ['console', 'mail_admins',],
                'level': DJANGO_REQUEST_LOG_LEVEL,
                'propagate': True
            },
            # 'django.server': {
            #     'handlers': ['django.server'],
            #     'level': DJANGO_SERVER_LOG_LEVEL,
            #     'propagate': False,
            # }
        },
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
