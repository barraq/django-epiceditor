from django import forms
from widgets import AdminPagedownWidget

class EpicEditorForm(forms.Form):
    """ An example form that includes the javascript required
    for EpicEditor automatically """
    
    body = forms.CharField(widget=AdminEpicEditorWidget())