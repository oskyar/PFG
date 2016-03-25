# encoding:utf-8
from urllib.parse import urlparse

from django.utils.translation import ugettext_lazy as _
from unipath import Path
import dj_database_url

LANGUAGES = (
    ('en-us', _('English')),
    ('es-es', _('Spanish')),
)

RUTA_PROYECTO = Path(__file__).ancestor(1)

# Additional locations of static files
LOCALE_PATHS = (
    RUTA_PROYECTO.child('locale'),
)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
# AUTH_USER_MODEL = 'user.UserProfile'
MANAGERS = ADMINS

# Database
DATABASES = {
    'heroku': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'ec2-54-163-228-188.compute-1.amazonaws.com',
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db36m2apq991b3',  # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'xbtoriyffsjctr',
        'PASSWORD': 'XriE7WjU6ZWDHYjB54k5D9XQCZ',
        # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
        'PORT': '5432',  # Set to empty string for default.
    },
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dbtfg',  # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'oskyar',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
        'PORT': '5432',  # Set to empty string for default.

    }
}

db_from_env = dj_database_url.config()
DATABASES['heroku'].update(db_from_env)

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']
DEBUG = True
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'CET'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-es'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = RUTA_PROYECTO.child("media")
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = 'staticfiles'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = [
    RUTA_PROYECTO.child('static'),

    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
]

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'n#5rx=e_(96f7%h03w*oggsfk87tbh@l7=3xfa!yi%)^i&hn14'

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'TFG.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'TFG.wsgi.application'

"""TEMPLATE_DIRS = [
    RUTA_PROYECTO.child('templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
]"""

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [RUTA_PROYECTO.child("templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': ["django.template.context_processors.i18n",
                                   "django.template.context_processors.request",
                                   "django.contrib.auth.context_processors.auth"],
            'debug': DEBUG,
        },
    }
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'TFG.apps.index',
    'TFG.apps.user',
    'TFG.apps.subject',
    'registration',
    'ajaxuploader'
)

from django.core.urlresolvers import reverse_lazy

LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('login')
# LOGOUT_URL = reverse_lazy('logout')

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Días para poder activar la cuenta
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True
# REGISTRATION_FORM = "user/register"
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
