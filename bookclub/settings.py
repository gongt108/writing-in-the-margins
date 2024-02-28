from pathlib import Path
import psycopg2
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(os.path.join(BASE_DIR, "bookscraper"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# using gmail
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # own
    "base",
    "users",
    "bookscraper",
    # tailwind
    "tailwind",
    "theme",
    "crispy_forms",
    "crispy_tailwind",
    "django_browser_reload",
    # other apps
    "django_rq",
]

TAILWIND_APP_NAME = "theme"
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

INTERNAL_IPS = [
    "127.0.0.1",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = "bookclub.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "bookclub.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "project4",
        "USER": "tiffanygong",
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": "localhost",
        "PORT": 5432,
    }
}

import dj_database_url

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES["default"].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
# STATIC_ROOT = [os.path.join(BASE_DIR, "static")]
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

RQ_QUEUES = {
    "default": {
        "HOST": "localhost",
        "PORT": 6379,
        "DB": 0,
        "USERNAME": "some-user",
        "PASSWORD": "some-password",
        "DEFAULT_TIMEOUT": 360,
        "REDIS_CLIENT_KWARGS": {  # Eventual additional Redis connection arguments
            "ssl_cert_reqs": None,
        },
    },
    "with-sentinel": {
        "SENTINELS": [("localhost", 26736), ("localhost", 26737)],
        "MASTER_NAME": "redismaster",
        "DB": 0,
        # Redis username/password
        "USERNAME": "redis-user",
        "PASSWORD": "secret",
        "SOCKET_TIMEOUT": 0.3,
        "CONNECTION_KWARGS": {  # Eventual additional Redis connection arguments
            "ssl": True
        },
        "SENTINEL_KWARGS": {  # Eventual Sentinel connection arguments
            # If Sentinel also has auth, username/password can be passed here
            "username": "sentinel-user",
            "password": "secret",
        },
    },
    "high": {
        "URL": os.getenv(
            "REDISTOGO_URL", "redis://localhost:6379/0"
        ),  # If you're on Heroku
        "DEFAULT_TIMEOUT": 500,
    },
    "low": {
        "HOST": "localhost",
        "PORT": 6379,
        "DB": 0,
    },
}

RQ_EXCEPTION_HANDLERS = ["path.to.my.handler"]  # If you need custom exception handlers
