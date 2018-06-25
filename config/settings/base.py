"""
Base settings to build other settings files upon.
"""

import os
import datetime
import environ

ROOT_DIR = environ.Path(__file__) - 3  # (sparta_webapp/config/settings/base.py - 3 = sparta_webapp/)
APPS_DIR = ROOT_DIR.path('sparta_webapp')

env = environ.Env()

READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR.path('.env')))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', True)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = 'UTC'
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres:///sparta_webapp'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'config.urls'
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# APPS
# ------------------------------------------------------------------------------
JET_APPS = [
    'jet.dashboard',
    'jet',
]

TEMPLATE_APPS = [
    'bootstrap_toolkit',
    'bootstrap4',
    'bootstrapform',
    'djedi',
]

DJANGO_APPS = [
    'django_assets',
    'django_tables2',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.humanize', # Handy template tags
    'django.contrib.admin',
]
THIRD_PARTY_APPS = [
    'crispy_forms',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.bitbucket',
    'allauth.socialaccount.providers.slack',
    'allauth.socialaccount.providers.paypal',
    'allauth.socialaccount.providers.amazon',
    'rest_framework',
    'rest_framework.authtoken',
]
LOCAL_APPS = [
    'sparta_webapp.users.apps.UsersAppConfig',
    # Your stuff: custom apps go here
    'sparta_webapp.apis.apps.ApiAppConfig',
    'sparta_webapp.eventlog.apps.EventLogAppConfig',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = JET_APPS + DJANGO_APPS + TEMPLATE_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# SOCIALACCOUNT PROVIDERS
# ------------------------------------------------------------------------------
# http://django-allauth.readthedocs.io/en/latest/providers.html

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
    },
    'paypal': {
        'SCOPE': ['openid', 'email'],
        'MODE': 'live',
    }
}

# REST Framework
# ------------------------------------------------------------------------------
# http://www.django-rest-framework.org/

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
}

# JWT_AUTH Settings
# ------------------------------------------------------------------------------
# http://getblimp.github.io/django-rest-framework-jwt/

JWT_AUTH = {
    "JWT_ENCODE_HANDLER":
    "rest_framework_jwt.utils.jwt_encode_handler",

    "JWT_DECODE_HANDLER":
    "rest_framework_jwt.utils.jwt_decode_handler",

    "JWT_PAYLOAD_HANDLER":
    "rest_framework_jwt.utils.jwt_payload_handler",

    "JWT_PAYLOAD_GET_USER_ID_HANDLER":
    "rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler",

    "JWT_RESPONSE_PAYLOAD_HANDLER":
    "rest_framework_jwt.utils.jwt_response_payload_handler",

    "JWT_SECRET_KEY": env('DJANGO_SECRET_KEY', default='CitKtCxzWd8tMP3v59FZrWdheZoU519tzoW7b52WdDKasn9JZEl5qJfKYnx3RJlg'),
    "JWT_GET_USER_SECRET_KEY": None,
    "JWT_PUBLIC_KEY": None,
    "JWT_PRIVATE_KEY": None,
    "JWT_ALGORITHM": "HS256",
    "JWT_VERIFY": True,
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_LEEWAY": 0,
    "JWT_EXPIRATION_DELTA": datetime.timedelta(seconds=900),
    "JWT_AUDIENCE": None,
    "JWT_ISSUER": None,

    "JWT_ALLOW_REFRESH": False,
    "JWT_REFRESH_EXPIRATION_DELTA": datetime.timedelta(days=7),

    "JWT_AUTH_HEADER_PREFIX": "JWT",
    "JWT_AUTH_COOKIE": "AuthToken",
}

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {
    'sites': 'sparta_webapp.contrib.sites.migrations'
}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = 'users.User'
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = 'users:redirect'
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = 'account_login'

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
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

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
    # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    # https://bitbucket.org/tkhyn/djinga
    #'BACKEND': 'djinga.backends.djinga.DjingaTemplates',
    # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
    'DIRS': [
        str(APPS_DIR.path('templates')),
    ],
    'OPTIONS': {
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
        'debug': DEBUG,
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
        # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
        #'load_from': ('sparta_webapp.templatetags.djingatags',),
        'loaders': [
            'apptemplates.Loader',
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
            'admin_tools.template_loaders.Loader',
        ],
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
            'sparta_webapp.context_processors.settings',
        ],
    },
    },
]
# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
DEFAULT_FROM_EMAIL = 'andrewvitko@gmail.com'
CONTACT_EMAIL = 'andrewvitko@gmail.com'

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = 'admin/'
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ("""Andrew Vitko""", 'andrew.vitko@spartasystems.com'),
]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# Celery
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['sparta_webapp.taskapp.celery.CeleryAppConfig']
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='django://')
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
if CELERY_BROKER_URL == 'django://':
    CELERY_RESULT_BACKEND = 'redis://'
else:
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ['json']
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = 'json'
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = 'json'
# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool('DJANGO_ACCOUNT_ALLOW_REGISTRATION', True)
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = 'username'
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ADAPTER = 'sparta_webapp.users.adapters.AccountAdapter'
# https://django-allauth.readthedocs.io/en/latest/configuration.html
SOCIALACCOUNT_ADAPTER = 'sparta_webapp.users.adapters.SocialAccountAdapter'

# Jet App
# ------------------------------------------------------------------------------
JET_THEMES = [
    {
       'theme': 'default', # theme folder name
       'color': '#47bac1', # color of the theme's button in user menu
       'title': 'Default' # theme title
    },
    {
       'theme': 'green',
       'color': '#44b78b',
       'title': 'Green'
    },
    {
       'theme': 'light-green',
       'color': '#2faa60',
       'title': 'Light Green'
    },
    {
       'theme': 'light-violet',
       'color': '#a464c4',
       'title': 'Light Violet'
    },
    {
       'theme': 'light-blue',
       'color': '#5EADDE',
       'title': 'Light Blue'
    },
    {
       'theme': 'light-gray',
       'color': '#222',
       'title': 'Light Gray'
    }
]

JET_DEFAULT_THEME = 'light-blue'

JET_INDEX_DASHBOARD = 'jet.dashboard.dashboard.DefaultIndexDashboard'

JET_APP_INDEX_DASHBOARD = 'jet.dashboard.dashboard.DefaultAppIndexDashboard'

# UserKey Values
# ------------------------------------------------------------------------------
SSHKEY_ALLOW_EDIT = True

SSHKEY_AUTHORIZED_KEYS_OPTIONS = ""

DEFAULT_HASH = "md5"
