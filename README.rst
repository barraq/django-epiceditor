django-epiceditor
=================

A django app that allows the easy addition of EpicEditor_ markdown editor to a django form field, whether in a custom app or the Django Admin.

.. _EpicEditor: http://oscargodson.github.com/EpicEditor/

Preview
-------

Here are a few screenshots of EpicEditor within django.

Standard edition mode
~~~~~~~~~~~~~~~~~~~~~

.. image:: https://raw.github.com/barraq/django-epiceditor/master/editor.png
    :alt: A screenshot of EpicEditor standard edition mode in Django's admin

Fullscreen edition mode mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: https://raw.github.com/barraq/django-epiceditor/master/fullscreen.png 
    :alt: A screenshot of EpicEditor fullscree mode in Django's admin")


Installation
------------

- Install via pip: `pip install -e https://github.com/barraq/django-epiceditor.git#egg=django-epiceditor` for the latest version, otherwise 'pip install django-epiceditor' 
- Add `epiceditor` to your `INSTALLED_APPS`

.. note:: This package will install a cloned copy of the EpicEditor_ library from https://github.com/OscarGodson/EpicEditor


Usage
-----

If you want to use the EpicEditor editor in a django admin field, there are numerous possible approaches:

To use it in **all** `TextField`'s in you admin form:

.. code:: python

    from django.db import models
    from epiceditor.widgets import AdminEpicEditorWidget
        
    class FooModelAdmin(models.ModelAdmin):
        formfield_overrides = {
            models.TextField: {'widget': AdminEpicEditorWidget },
        }
        
Alternatively, to only use it on particular fields, first create a form (in `forms.py`): 

.. code:: python

    from django import forms
    from models import FooModel
    from epiceditor.widgets import AdminEpicEditorWidget    
    class FooModelForm(forms.ModelForm):
        a_text_field = forms.CharField(widget=AdminEpicEditorWidget())      
        another_text_field = forms.CharField(widget=AdminEpicEditorWidget())    
        
        class Meta:
            model = FooModel
            
and in your `admin.py`:

.. code:: python

    from forms import FooModelForm
    
    class FooModelAdmin(models.ModelAdmin):
        form = FooModelForm   
 
Themes
~~~~~~

EpicEditor_ comes with different themes. In order to change the default themes EpicEditorWidget 
allows you to pass *themes* parameters. For instance if you want to use the light theme for the editor do as
follow:

.. code:: python

    from django import forms
    from models import FooModel
    from epiceditor.widgets import AdminEpicEditorWidget    
    class FooModelForm(forms.ModelForm):
        a_text_field = forms.CharField(widget=AdminEpicEditorWidget(themes={'editor':'epic-light.css'}))      
        another_text_field = forms.CharField(widget=AdminEpicEditorWidget())    
        
        class Meta:
            model = FooModel
 
Notes
-----

This plugin was develop by taking inspiration from django-pagedown_ and is using the great EpicEditor_.

.. _django-pagedown: https://github.com/timmyomahony/django-pagedown
