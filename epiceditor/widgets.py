from django import forms
from django.conf import settings
from django.contrib.admin import widgets as admin_widgets
from django.forms.widgets import flatatt
from django.utils.html import conditional_escape, escapejs
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe


class EpicEditorWidget(forms.Textarea):
    def __init__(self, theme_base='epiceditor.css', theme_preview='preview-dark.css', theme_editor='epic-dark.css', attrs=None):
        self.theme_base = '/themes/base/' + theme_base
        self.theme_preview = '/themes/preview/' + theme_preview
        self.theme_editor = '/themes/editor/' + theme_editor
        super(EpicEditorWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        html = """
            <div id="%(id)sepiceditor"></div>
            <textarea%(attrs)s>%(body)s</textarea>
            <script type="text/javascript">
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
                    $textarea = $('#%(id)s');
                    $textarea.hide();
                    // then be sure to populate the textarea
                    editor.on('update', function (file) {
                      $textarea.val(file.content);
                    });

                    // Everything is all setup, so load!
                    editor.load();
                  });
                })(django.jQuery);
            </script>
            """ % {
                'basePath': (settings.STATIC_URL or settings.MEDIA_URL) + 'epiceditor',
                'defaultContent': escapejs(force_unicode(value)),
                'theme_base': self.theme_base,
                'theme_preview': self.theme_preview,
                'theme_editor': self.theme_editor,
                'attrs': flatatt(final_attrs),
                'body': conditional_escape(force_unicode(value)),
                'id': attrs['id'],
            }
        return mark_safe(html)

    class Media:
        js = (
            (settings.STATIC_URL or settings.MEDIA_URL) + 'epiceditor/js/epiceditor.min.js',
        )


class AdminEpicEditorWidget(admin_widgets.AdminTextareaWidget, EpicEditorWidget):
    def __init__(self, attrs=None, **kargs):
        super(AdminEpicEditorWidget, self).__init__(attrs, **kargs)
