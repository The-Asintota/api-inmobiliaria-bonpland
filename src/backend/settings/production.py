from .base import *
import dj_database_url
import os


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [config('TEST'), config('SERVER_HOST')]

CSRF_TRUSTED_ORIGINS = [f'https://{config("SERVER_HOST")}']


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(
        default=config('POSTGRE_DB_URL')
    ),
    'mongo_db': {
        'NAME': config('MDB_NAME_PRODUCTION'),
        'HOST': config('MDB_HOST_PRODUCTION'),
        'PORT': int(config('MDB_PORT_PRODUCTION')),
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = 'static/'

STATIC_ROOT = os.path.join('app', 'static')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Cors settings
CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = [f'https://{config("TEST")}']


# drf-spectacular settings
SPECTACULAR_SETTINGS['SERVERS'] = [
    {
        'url': f'https://{config("SERVER_HOST")}/',
        'description': 'FL0 Server'
    }
]
