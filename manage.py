#!/usr/bin/env python
import os
import sys
from flight.project_environment import PROJECT_ENV
from flight.default_values import (PRODUCTION_ENVIRONMENT,
                                   DEVELOPMENT_ENVIRONMENT
                                   )

if __name__ == '__main__':
    if PROJECT_ENV==PRODUCTION_ENVIRONMENT:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight.settings.production_settings')
    elif PROJECT_ENV==DEVELOPMENT_ENVIRONMENT:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight.settings.development_settings')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight.settings.local_settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
