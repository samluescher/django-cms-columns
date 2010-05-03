from django.utils.translation import ugettext as _

CMS_COLUMNS_CSS_FRAMEWORK = 'yaml'

CMS_COLUMNS_TEMPLATE = 'cms_columns/column.%(framework)s.html'

CMS_COLUMNS_WIDTH_CHOICES = (
    ('100', _('Full page width')),
    ('75', _('%s%% wide') % '75'),
    ('66', _('%s%% wide') % '66'),
    ('50', _('%s%% wide') % '50'),
    ('33', _('%s%% wide') % '33'),
    ('25', _('%s%% wide') % '25'),
)
