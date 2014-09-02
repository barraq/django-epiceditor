from django import forms
from django.conf import settings
from django.contrib.admin import widgets as admin_widgets
from django.forms.widgets import flatatt
from django.utils.html import conditional_escape, escapejs
try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text
from django.utils.safestring import mark_safe



EPICEDITOR_DEFAULT_THEMES = {
    'base': 'epiceditor.css',
    'preview': 'preview-dark.css', 
    'editor': 'epic-dark.css'}



class EpicEditorWidget(forms.Textarea):
    def __init__(self, attrs=None, themes=None):
        final_themes = EPICEDITOR_DEFAULT_THEMES
        if themes is not None:
            final_themes.update(themes)
        self.themes = dict([(k,'/themes/%s/%s' % (k,v)) for k,v in final_themes.items()])
        super(EpicEditorWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        html = """
            <div id="%(id)sepiceditor"></div>
            <textarea%(attrs)s>%(body)s</textarea>
            <script type="text/javascript">
                var ee = {
                    'jQuery': (typeof window.django != 'undefined') ? django.jQuery : jQuery.noConflict(true)
                };

                (function($) {
                  $(document).ready(function() {
                    var opts = {
                        container: '%(id)sepiceditor',
                        basePath: '%(basePath)s',
                        theme: {
                          base:'%(theme_base)s',
                          preview:'%(theme_preview)s',
                          editor:'%(theme_editor)s'
                        },
                        file:{
                          defaultContent: "%(defaultContent)s",
                        },
                        clientSideStorage: false,
                        useNativeFullsreen: true,
                        parser: marked,
                        focusOnLoad: false,
                        shortcut: {
                            modifier: 18,
                            fullscreen: 70,
                            preview: 80
                        }
                    }
                    var editor = new EpicEditor(opts);

                    // get textarea and hide it
                    %(textarea)s = $('#%(id)s');
                    %(textarea)s.hide();
                    // then be sure to populate the textarea
                    editor.on('update', function () {
                      %(textarea)s.val(editor.exportFile());
                    });

                    // Everything is all setup, so load!
                    editor.load();
                  });
                })(ee.jQuery);
            </script>
            """ % {
                'basePath': (settings.STATIC_URL or settings.MEDIA_URL) + 'epiceditor',
                'defaultContent': escapejs(force_text(value)),
                'theme_base': self.themes['base'],
                'theme_preview': self.themes['preview'],
                'theme_editor': self.themes['editor'],
                'attrs': flatatt(final_attrs),
                'body': conditional_escape(force_text(value)),
                'id': attrs['id'],
                'textarea': "$textarea_" + attrs['id'].replace('-', '_'),
            }
        return mark_safe(html)

    class Media:
        js = (
            (settings.STATIC_URL or settings.MEDIA_URL) + 'epiceditor/js/epiceditor.min.js',
        )


class AdminEpicEditorWidget(EpicEditorWidget, admin_widgets.AdminTextareaWidget):
    def __init__(self, attrs=None, themes=None):
        super(AdminEpicEditorWidget, self).__init__(attrs, themes)
