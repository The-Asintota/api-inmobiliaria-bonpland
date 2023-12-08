from .base import *
import dj_database_url
import os


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [config('URL_TEST'), config('URL_SERVER')]

CSRF_TRUSTED_ORIGINS = [config('URL_SERVER')]


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATA_BASE_URL')
    )
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = 'static/'

STATIC_ROOT = os.path.join('app', 'static')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Cors settings
CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = [config('URL_TEST')]


# drf-spectacular settings
SPECTACULAR_SETTINGS['SERVERS'] = [
    {
        'url':f'{config("URL_SERVER")}/',
        'description':'FL0 Server'
    }
]