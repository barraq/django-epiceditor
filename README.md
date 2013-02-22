django-epiceditor
=================

A django app that allows the easy addition of [EpicEditor](http://oscargodson.github.com/EpicEditor/) markdown editor to a django form field, whether in a custom app or the Django Admin.


---

## Preview

Here are a few screenshots of EpicEditor within django.

### Edition mode

![Screenshot of Django Admin with EpicEditor initialised](https://raw.github.com/barraq/django-epiceditor/master/editor.png "A screenshot of EpicEditor edition mode in Django's admin")

### Fullscreen mode

![Screenshot of Django Admin with EpicEditor initialised](https://raw.github.com/barraq/django-epiceditor/master/fullscreen.png "A screenshot of EpicEditor fullscree mode in Django's admin")


## Installation

- Install via pip: `pip install -e https://github.com/barraq/django-epiceditor.git#egg=django-epiceditor` for the latest version, otherwise 'pip install django-epiceditor' 
- Add `epiceditor` to your `INSTALLED_APPS`

Note that this package will install a cloned copy of the EpicEditor library from [https://github.com/OscarGodson/EpicEditor](https://github.com/OscarGodson/EpicEditor)


## Usage ##

If you want to use the EpicEditor editor in a django admin field, there are numerous possible approaches:

To use it in **all** `TextField`'s in you admin form:

	from django.db import models
	from epiceditor.widgets import AdminEpicEditorWidget
		
    class FooModelAdmin(models.ModelAdmin):
    	formfield_overrides = {
        	models.TextField: {'widget': AdminEpicEditorWidget },
    	}
    	
Alternatively, to only use it on particular fields, first create a form (in `forms.py`): 

	from django import forms
	from models import FooModel
	from epiceditor.widgets import AdminEpicEditorWidget	
	class FooModelForm(forms.ModelForm):
		a_text_field = forms.CharField(widget=AdminEpicEditorWidget())		
		another_text_field = forms.CharField(widget=AdminEpicEditorWidget())	
		
		class Meta:
			model = FooModel
			
and in your `admin.py`:

	from forms import FooModelForm
	
    class FooModelAdmin(models.ModelAdmin):
    	form = FooModelForm   
 
 
## Notes ##
   	
This plugin was develop by taking inspiration from [django-pagedown](https://github.com/timmyomahony/django-pagedown) and is using the great [EpicEditor](https://github.com/OscarGodson/EpicEditor).