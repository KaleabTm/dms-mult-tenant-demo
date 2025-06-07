import os

from config.env import APPS_DIR, BASE_DIR, env

env.read_env(os.path.join(BASE_DIR, ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-eb7x*euse3jj879p3vtb_^gbolpga@rl$18pqnn93@t0n*@!$a"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=True)  # type: ignore

ALLOWED_HOSTS = ["*"]

# --- Third-Party Apps ---
SHARED_THIRD_PARTY_APPS = [
    "corsheaders",
    "drf_spectacular",
    "django_extensions",
    "django_filters",
    "easyaudit",
    "rest_framework",
    "django_tenants",
    "import_export",  # Shared for both, but should only be listed in SHARED
]

TENANT_THIRD_PARTY_APPS = [
    "guardian",  # Only needed in tenants
]

# --- Local Apps ---
SHARED_LOCAL_APPS = [
    "core.api.apps.ApiConfig",  # if schema-aware, otherwise move to tenant
    "core.authentication.apps.AuthenticationConfig",
    "core.users.apps.UsersConfig",  # shared user model across schemas
    "core.common.apps.CommonConfig",
    "core.tenants.apps.TenantsConfig",  # MUST be here, contains Tenant & Domain
]

TENANT_LOCAL_APPS = [
    "core.contacts.apps.ContactsConfig",
    "core.departments.apps.DepartmentsConfig",
    "core.emails.apps.EmailsConfig",
    "core.posts.apps.PostsConfig",
]

# --- Final Grouping ---
SHARED_APPS = [
    # Django core
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # Shared third-party and local
    *SHARED_THIRD_PARTY_APPS,
    *SHARED_LOCAL_APPS,
]

TENANT_APPS = [
    *TENANT_THIRD_PARTY_APPS,
    *TENANT_LOCAL_APPS,
]

# --- Installed Apps: Shared First, Avoid Duplicates ---
INSTALLED_APPS = SHARED_APPS + [app for app in TENANT_APPS if app not in SHARED_APPS]


TENANT_MODEL = "tenants.Tenant"

TENANT_DOMAIN_MODEL = "tenants.Domain"


MIDDLEWARE: list[str] = [
    "django_tenants.middleware.main.TenantMainMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "easyaudit.middleware.easyaudit.EasyAuditMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(APPS_DIR, "templates")],
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

WSGI_APPLICATION = "config.wsgi.application"

ASGI_APPLICATION = "config.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django_tenants.postgresql_backend",
        "NAME": env.str("DB_NAME"),
        "USER": env.str("DB_USER"),
        "PASSWORD": env.str("DB_PASSWORD"),
        "HOST": env.str("DB_HOST"),
        "PORT": env.str("DB_PORT"),
    },
}


DATABASE_ROUTERS = ("django_tenants.routers.TenantSyncRouter",)


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = "users.User"

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "core.api.exception_handler.drf_exception_handler",
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

APP_DOMAIN = env("APP_DOMAIN", default="http://localhost:8000")  # type: ignore

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
)

ANONYMOUS_USER_NAME = None
GUARDIAN_GET_CONTENT_TYPE = "polymorphic.contrib.guardian.get_polymorphic_base_content_type"

from config.settings.logging import *  # noqa
from config.settings.cors import *  # noqa
from config.settings.files_and_storages import *  # noqa
from config.settings.sessions import *  # noqa

from config.settings.debug_toolbar.settings import *  # noqa
from config.settings.debug_toolbar.setup import DebugToolbarSetup  # noqa

INSTALLED_APPS, MIDDLEWARE = DebugToolbarSetup.do_settings(INSTALLED_APPS, MIDDLEWARE)

SPECTACULAR_SETTINGS = {
    "TITLE": "Django API Template",
    "DESCRIPTION": "A reusable template for creating Django APIs quickly and efficiently. Includes best practices, configurations, and initial setup to jump start your Django projects.",  # noqa: E501
    "VERSION": "1.0.0",
}

SHOW_PUBLIC_IF_NO_TENANT_FOUND = True
