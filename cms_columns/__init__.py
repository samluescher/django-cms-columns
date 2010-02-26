import register_model 
from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import FieldDoesNotExist
from cms_columns.models import AbstractColumn, TextColumn
from cms_columns.cms_plugins import TextColumnPlugin
from django.utils.translation import ugettext as _

CONTRIBUTE_FIELDS = ['column_width',]

def register(model, plugin=None):
    for field_name in CONTRIBUTE_FIELDS:
        field = AbstractColumn._meta.get_field(field_name)
        try:
            model._meta.get_field(field.attname)
        except FieldDoesNotExist:
            field.contribute_to_class(model, field.attname)
    if plugin:
        if hasattr(plugin, 'fieldsets') and plugin.fieldsets:
            plugin.fieldsets.append((_('Column'), {'fields': CONTRIBUTE_FIELDS}))

def get_model_from_string(model_path):
    app_label, model_name = model_path.rsplit('.models.')
    return models.get_model(app_label, model_name)

if hasattr(settings, 'CMS_COLUMNS_REGISTER_MODELS'):
    for item in settings.CMS_COLUMNS_REGISTER_MODELS:
        if not isinstance(item, tuple):
            item = (item,)
        model_path = item[0]
        model = get_model_from_string(model_path)
        if len(item) > 1:
            from cms.plugin_pool import plugin_pool
            app_label, plugin_name = item[1].rsplit('.cms_plugins.')
            plugin = plugin_pool.get_plugin(plugin_name)
        else:
            plugin = None
        if not model:
            raise ImproperlyConfigured('Model %s cannot be imported' % model_path)
        else:
            register(model, plugin)

register(TextColumn, TextColumnPlugin)
