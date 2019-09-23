"""
WSGI config for flight project by Mohammad Rezaei.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from flight.project_environment import PROJECT_ENV
from flight.default_values import (PRODUCTION_ENVIRONMENT,
                                   DEVELOPMENT_ENVIRONMENT
                                   )

if PROJECT_ENV == PRODUCTION_ENVIRONMENT:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight.settings.production_settings')
elif PROJECT_ENV == DEVELOPMENT_ENVIRONMENT:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight.settings.development_settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight.settings.local_settings')

application = get_wsgi_application()
