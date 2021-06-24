import os
from configparser import ConfigParser
from django.contrib.messages import constants as messages


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(BASE_DIR, "config.ini")

config = ConfigParser(interpolation=None)
config.read(CONFIG_FILE)

SECRET_KEY = config.get("core", "SECRET_KEY")
DEBUG = config.getboolean("core", "DEBUG")
ALLOWED_HOSTS = config.get("core", "ALLOWED_HOSTS").split("|")

NAME_REGEX = r"^[A-Za-zÁÇÉÍÓÚÑÜáçéíóúñü\.\,\'\-\ ]+$"
PASSWORD_REGEX = r"^.*(?=.{8,})(?=.*\d)(?=.*[a-zA-Z]).*$"
PASSWORD_RESET_TIMEOUT_DAYS = 1

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_forms",
    "django_crontab",
    "django_countries",
    "common",
    "accounts",
    "partners",
    "invoices",
    "projects",
    "servers",
]
CRONJOBS = [
    (
        "0 * * * *",
        "invoices.cron.update_invoices_status",
        "2>&1 | /usr/bin/logger -t BUSINESS_TRACKER",
    )
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "common.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

TEMPLATES[0]["OPTIONS"]["context_processors"].append(
    "invoices.context_processors.review_invoices_processor"
)

WSGI_APPLICATION = "common.wsgi.application"
if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": config.get("database", "DATABASE_NAME") + ".sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": config.get("database", "DATABASE_NAME"),
            "USER": config.get("database", "DATABASE_USER"),
            "PASSWORD": config.get("database", "DATABASE_PASSWORD"),
            "HOST": "localhost",
            "PORT": "",
        }
    }

LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"

USE_I18N = False
USE_L10N = False
USE_TZ = False

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

if DEBUG:
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
else:
    STATIC_ROOT = config.get("core", "STATIC_ROOT")
    MEDIA_ROOT = config.get("core", "MEDIA_ROOT")

MESSAGE_TAGS = {
    messages.DEBUG: "dark",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}
CRISPY_TEMPLATE_PACK = "bootstrap4"
AUTH_USER_MODEL = "accounts.Account"

TEMPLATE_FILE = os.path.join("example_template.pdf")
