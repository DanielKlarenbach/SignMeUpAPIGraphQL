import os

if os.environ.get('DJANGO_DEPLOYMENT'):
    from .deployment_settings import *
else:
    from .production_settings import *