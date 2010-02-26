from django.conf import settings
from cms_columns import defaults

def get(key):
    if hasattr(settings, key):
        return getattr(settings, key)
    else:
        return getattr(defaults, key)
