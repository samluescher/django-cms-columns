from django.conf import settings

def get_auto_thumbnail_size(column_width):
    dict = {}
    if hasattr(settings, 'CMS_COLUMNS_GRID_WIDTH') and hasattr(settings, 'CMS_COLUMNS_GRID_WIDTH_PX'):
        grid_spans = int(column_width) / settings.CMS_COLUMNS_GRID_WIDTH
        width = grid_spans * settings.CMS_COLUMNS_GRID_WIDTH_PX
        if hasattr(settings, 'CMS_COLUMNS_GUTTER_WIDTH_PX'):
            width += (grid_spans - 1) * settings.CMS_COLUMNS_GUTTER_WIDTH_PX
        
        dict.update({
            'thumbnail_size': '%sx%s' % (width, width),
            'column_width_px': width,
        })

    return dict

def auto_thumbnail_size(request):
    """
    Adds a variable `thumbnail_size` to context for 100% column width,
    according to the CMS_COLUMNS_GRID_WIDTH and CMS_COLUMNS_GRID_WIDTH_PIXELS settings.
    """
    return get_auto_thumbnail_size(100)