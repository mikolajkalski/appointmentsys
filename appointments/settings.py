
import os
from pathlib import Path

from django.conf import locale
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-(%st!9pc%2d%*b3xt8@0o7*4rkxq-$6j3y-(b*ftz^m2^r4l$z"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "appointment.apps.AppointmentConfig",
]

# if you want to use Django Q for sending emails asynchronously, you must install django-q2 in your env
if os.environ.get('USE_DJANGO_Q', 'False').lower() == 'true':
    INSTALLED_APPS.append('django_q')

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.middleware.locale.LocaleMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "appointments.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'appointment/templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "appointments.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en"

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "appointment/static")]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

APPOINTMENT_BUFFER_TIME = 0

LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]
LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
    # ('es', _('Spanish')), # uncomment to add Spanish
)

# Email Configuration
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.example.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')

# Check
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False').lower() == 'true'

# If SSL is True, TLS will be set to False
# Can't have both SSL and TLS set to True :(
if EMAIL_USE_SSL:
    EMAIL_USE_TLS = False
    # Default SSL port if not specified is 465
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 465))

EMAIL_SUBJECT_PREFIX = os.getenv('EMAIL_SUBJECT_PREFIX', '')
EMAIL_USE_LOCALTIME = os.getenv('EMAIL_USE_LOCALTIME', 'True').lower() == 'true'
SERVER_EMAIL = os.getenv('SERVER_EMAIL', EMAIL_HOST_USER)
USE_DJANGO_Q_FOR_EMAILS = os.getenv('USE_DJANGO_Q_FOR_EMAILS', 'True').lower() == 'true'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)

# Little warning if EMAIL_HOST_USER or EMAIL_HOST_PASSWORD is not set
# This won't appear in the console when using the package, only when running the Django project or docker-compose
if not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD:
    print("Warning: EMAIL_HOST_USER or EMAIL_HOST_PASSWORD is not set. Email functionality may be limited.")

# Warn if both TLS and SSL are set to True (only appears when running the Django project or docker-compose)
# To be honest, this would be unique if you do this in your .env, I mean, come on :(
if EMAIL_USE_TLS and EMAIL_USE_SSL:
    print("Warning: Both EMAIL_USE_TLS and EMAIL_USE_SSL are set to True. Only SSL will be used.")

# ADMINS configuration
ADMIN_NAME = os.getenv('ADMIN_NAME', 'Admin')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', '')
ADMINS = [(ADMIN_NAME, ADMIN_EMAIL)] if ADMIN_EMAIL else []

# Same as above, only appears when running the Django project or docker-compose
if not ADMIN_EMAIL:
    print("Warning: ADMIN_EMAIL is not set. Error emails will not be sent to administrators.")

# if using Django Q, example of extra configuration (you can change this to your liking)
if 'django_q' in INSTALLED_APPS:
    Q_CLUSTER = {
        'name': 'django-appointment',
        'workers': 4,
        'timeout': 90,
        'retry': 120,
        'queue_limit': 50,
        'bulk': 10,
        'orm': 'default',
        'redis': {
            'host': 'redis',
            'port': 6379,
            'db': 0,
        }
    }
