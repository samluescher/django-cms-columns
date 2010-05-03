from django.conf import settings 
from cms_columns import context_processors

"""
Adds a variable `thumbnail_size` to context for the plugin's column width,
according to the CMS_COLUMNS_GRID_WIDTH and CMS_COLUMNS_GRID_WIDTH_PIXELS settings.
"""
def auto_thumbnail_size(instance, placeholder):
    dict = {}
    if (not hasattr(settings, 'CMS_COLUMNS_PLACEHOLDERS') \
        or placeholder.slot in settings.CMS_COLUMNS_PLACEHOLDERS):
            if hasattr(instance, 'column_width') and instance.column_width: 
                dict.update(context_processors.get_auto_thumbnail_size(instance.column_width))
            else:
                dict.update(context_processors.get_auto_thumbnail_size(100))
    return dict
