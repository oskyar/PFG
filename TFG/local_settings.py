import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
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

DEBUG = True
