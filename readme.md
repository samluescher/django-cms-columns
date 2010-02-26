Django CMS Columns
==================

A collection of tools to add abstract support for variable column width to your CMS plugins. For use with CSS frameworks that support grid layouts or subcolumns, such as [YAML](http://www.yaml.de/en/documentation/practice/subtemplates.html) or [Blueprint](http://www.blueprintcss.org/).

The goal of this application is to enable to you to assign a relative column width (percentage of total page width) to every plugin. Using this application, you can arrange blocks of content next to each other within a CMS placeholder.

How it works
------------

The `columns` plugin processor looks for an attribute `column_width` in each plugin instance. It then renders the original plugin output through a column template, including the context variables `column_width` and `last_column`. 

The column template is a template that wraps the original plugin output and makes it exactly as wide as specified. What it should look like depends on the CSS/framework you are using to create grid layouts.

__Example using the [YAML](http://www.yaml.de/en/documentation/practice/subtemplates.html) CSS framework__:

Suppose you have a CMS plugin called `HelloWorldPlugin`, which you put on your page twice. The original output produced by those two plugins looks as follows:

    <p>Hello, world!</p>
    <p>Hello again, world!</p>
    
Now you would like to have the second plugin appear not below the first one, but next to it, with one plugin occupying 75% of the page width and the other one filling up the remaining 25%. To achieve this, you install the `cms_columns` app, set the respective column widths, and let the following column template take care of the rest:  
    
    <!-- column.yaml.html -->
    {% if plugin.first %}
    <div class="subcolumns"> 
    {% endif %}
        <div class="c{{ column_width }}{% if last_column %}r{% else %}l{% endif %}">
            <div class="subc{% if last_column %}r{% else %}l{% endif %}">
                {{ content|safe }}
            </div>
        </div>
    {% if plugin.last %}
    </div>
    {% else %}
    {% if last_column %}
    </div>
    <div class="subcolumns">
    {% endif %}
    {% endif %}

Here's what the final output of the two plugins, rendered again through the column template, looks like:

    <div class="subcolumns"> 
        <div class="c75l">
            <div class="subcl">
                <p>Hello, world!</p>
            </div>
        </div>
        <div class="c25r">
            <div class="subcr">
                <p>Hello again, world!</p>
            </div>
        </div>
    </div>
 
Installation
------------

This document assumes that you are familiar with Python and Django.

1. Make sure `cms_columns` is on your `PYTHONPATH`.
2. Add `cms_columns` to `settings.INSTALLED_APPS`
3. Add `cms_columns.cms_plugin_processors.columns` to `settings.CMS_PLUGIN_PROCESSORS`
4. Optionally, if you want to resize images according to column widths:
Add `cms_columns.context_processors.auto_thumbnail_size` to `settings.TEMPLATE_CONTEXT_PROCESSORS`,
add `cms_columns.cms_plugin_context_processors.auto_thumbnail_size` to `settings.CMS_PLUGIN_CONTEXT_PROCESSORS`.

Usage and configuration
-----------------------

###Bundled CMS plugins###

By installing the application, two new plugins become available to Django CMS: `TextColumnPlugin` and `ManualBreakPlugin`. The former is basically the `Text` plugin with an additional field `column_width` that you can adjust when editing pages. The latter can be used to create a manual row break, in cases when you don't want to fill up the full page width with floating columns. These two plugins are ready to use and, in conjunction with the plugin processor, `cms_columns.cms_plugin_processors.columns`, should produce the desired results.

###Applying to 3rd-party plugins###

__`CMS_COLUMNS_REGISTER_MODELS`__

In order to add column widths to any installed CMS plugin, you can put `CMS_COLUMNS_REGISTER_MODELS` in your settings and add to it all plugins that you want to have column support:

    # settings.py
    CMS_COLUMNS_REGISTER_MODELS = (
        'cms.plugins.teaser.models.Teaser', 
        ('myapp.models.MySpecialPluginModel', 'myapp.cms_plugins.MySpecialPlugin'),
    )

This setting results in the `cms_columns.register()` method being called for the two plugins. That method adds the `column_width` field to each model. __Note that you also need to add this field to your database tables__ if you already set up your database.

Apart from the model, you can also specify the plugin class by putting an item in this setting that is a two-tuple (which is the case for the second item, `MySpecialPluginModel`). By doing this you are making sure that `column_width` will be editable if your plugin class contains [fieldsets](http://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets). 


###Additional settings###

__`CMS_COLUMNS_WIDTH_CHOICES`__

Using this setting you can define the values to choose from for the `column_width` field. By default these are 100, 75, 50 and 25. The value should be a two-tuple [as explained in the Django documentation](http://www.djangoproject.com/documentation/models/choices/). 

__`CMS_COLUMNS_PLACEHOLDERS`__

If you want to restrict the use of the `columns` plugin processor to specific placeholders, put the  respective placeholder names in this list.

__`CMS_COLUMNS_TEMPLATE = 'cms_columns/column.%(framework)s.html'`__

This is the name of the column template that produces your final output. Note that it may or may not contain the name of your CSS framework, which will be inserted using [string formatting](http://docs.python.org/library/stdtypes.html#string-formatting-operations). 

__`CMS_COLUMNS_CSS_FRAMEWORK = 'yaml'`__

The name of the CSS framework that you are using. This is currently only used to deduce the template name, but may be useful for other features in the future.

###Usage with your own CMS plugins###

If you are creating your own plugin that you want to have built-in column support, your plugin model only needs an additional `column_width` field. You can either add this field to your model yourself, or register the plugin model and plugin class with the `cms_columns` application. This has the same effect as putting the plugin in the `CMS_COLUMNS_REGISTER_MODELS` setting:

    # models.py
    import cms_columns

    class MyPluginModel:
        pass
    cms_columns.register(MyPluginModel)

Automatically fitting images into columns 
-----------------------------------------

A very handy feature of this application is the automatic calculation of thumbnail sizes according to column width. For instance, if you have four subcolumns, each of which are 170px wide (this is your grid width), and you would like to have a picture span three of those columns (or grid elements), you can use the following settings:

__`CMS_COLUMNS_GRID_WIDTH`__

Your grid width, i.e. the relative width of the smallest subcolumn you are using. In the example above, this would be `25`.

__`CMS_COLUMNS_GRID_WIDTH_PX`__

Your grid width in pixels, i.e. the absolute width of the smallest subcolumn you are using. In the example above, this would be `170`.

__`CMS_COLUMNS_GUTTER_WIDTH_PX`__ 

If there is a margin or “gutter” between your subcolumns, you can specify it here. In the example above, an image spanning three grid elements would have to be as wide as the grid width times three plus twice the gutter width (since there are two gutters between three grid elements). 

These three settings are used by the `auto_thumbnail_size` template context processor and plugin context processor also provided by this application. The processors do nothing more than adding the `thumbnail_size` variable to your context, which is a tuple containing the maximum width and height that a thumbnail should have in the given context. It is entirely up to you to use these dimensions in the template to properly resize your images.

__Example usage__ 

Staying with the example above, suppose our original image has a resolution of 1024×768. Our grid width is 170px and the gutter width is 18px. The plugin being rendered has a `column_width` of 75, meaning that the picture should span three columns. The `auto_thumbnail_size` processor populated the context with the variable `thumbnail_size = (546, 1092)` (because 3 × 170 + 2 * 18 = 546). This first element is how wide the image should be. The image should be scaled down maintaining aspect ratio, so it should have a height of 410px (because 546 / 1024 × 768 = 409.5). But how do we figure this out in the template? Luckily, Django comes with a built-in template tag called `widthratio` which does exactly this calculation:

    <!-- my-image-template.html -->
    <img src="{{ my_image.file.url }}" width="{{ thumbnail_size.0 }}" height="{% widthratio thumbnail_size.0 my_image.width my_image.height %}" />
    
The final output will be:

    <img src="static/my_image.jpg" width="546" height="410" />
    
__Example usage with sorl-thumbnail__

You're probably going to want to not only display a smaller image, but actually deliver a thumbnail to the client. One of the most popular solutions for this is [sorl-thumbnail](http://thumbnail.sorl.net/docs/). In this case you don't need to do any ratio calculations. Here's how you would use sorl-thumbnail with the `thumbnail_size` variable: 

    {% load thumbnail %}
    {% thumbnail my_image.file thumbnail_size as thumb %}
    <img src="{{ thumb }}" width="{{ thumb.width }}" height="{{ thumb.height }}" />

And we're done.