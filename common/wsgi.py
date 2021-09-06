import os
from configparser import InterpolationError, NoOptionError, NoSectionError

from django.core.wsgi import get_wsgi_application

os.environ["DJANGO_SETTINGS_MODULE"] = "common.settings"

try:
    application = get_wsgi_application()
except (NoSectionError, NoOptionError, InterpolationError):
    print("\033[91mInvalid config file\033[0m")
