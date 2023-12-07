"""
WSGI config for prueba project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from decouple import config


if config('ENVIRONMENT_STATUS') == 'development':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.local')
elif config('ENVIRONMENT_STATUS') == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.production')

application = get_wsgi_application()