from pathlib import Path
import os
import environ

# from os import environ


env = environ.Env()

USE_TZ = True

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")
# SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["127.0.0.1", "0.0.0.0", "localhost"]


# Application definition


INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.sites",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "froala_editor",
    "rest_framework",
    "crispy_forms",
    # 'taggit',
    "widget_tweaks",
    "home",
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

ROOT_URLCONF = "blog.urls"

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

WSGI_APPLICATION = "blog.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRESQL_DB"),
        "USER": env("POSTGRESQL_USER"),
        "PASSWORD": env("POSTGRESQL_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    "static",
]

MEDIA_URL = "/media/"
STATIC_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


FRAOLA_EDITOR_THIRD_PARTY = ("image_aviary", "spell_checker")
FROALA_EDITOR_PLUGINS = (
    "align",
    "char_counter",
    "code_beautifier",
    "code_view",
    "colors",
    "draggable",
    "emoticons",
    "entities",
    "file",
    "font_family",
    "font_size",
    "fullscreen",
    "image_manager",
    "image",
    "inline_style",
    "line_breaker",
    "link",
    "html",
    "lists",
    "paragraph_format",
    "paragraph_style",
    "quick_insert",
    "quote",
    "save",
    "table",
    "url",
    "video",
)

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_OPEN = True

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

<<<<<<< HEAD
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
=======
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_HOST")
EMAIL_HOST_USER = env("EMAIL_HOST")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST")
>>>>>>> 5e7e056 (refactoring)
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

FRAOLA_EDITOR_THIRD_PARTY = ("image_aviary", "spell_checker")
FROALA_EDITOR_PLUGINS = (
    "align",
    "char_counter",
    "code_beautifier",
    "code_view",
    "colors",
    "draggable",
    "emoticons",
    "entities",
    "file",
    "font_family",
    "font_size",
    "fullscreen",
    "image_manager",
    "image",
    "inline_style",
    "line_breaker",
    "link",
    "html",
    "lists",
    "paragraph_format",
    "paragraph_style",
    "quick_insert",
    "quote",
    "save",
    "table",
    "url",
    "video",
)

# AUTH_USER_MODEL = 'users.CustomUser'

<<<<<<< HEAD
SITE_ID=1
=======
SITE_ID = 1
>>>>>>> 5e7e056 (refactoring)
