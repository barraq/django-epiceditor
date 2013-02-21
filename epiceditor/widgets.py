from django import forms
from django.conf import settings
from django.contrib.admin import widgets as admin_widgets
from django.forms.widgets import flatatt
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe


class EpicEditorWidget(forms.Textarea):
    class Media:
        css = {
            'all': ('epiceditor/themes/base/epiceditor.css', 'epiceditor/themes/themes/preview/preview-dark.css', 'epiceditor/themes/preview/preview-dark.css')
        }
        js = ('%s/epiceditor/js/epiceditor.min.js' % settings.STATIC_URL,)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        html = """
            <div id="%(id)sepiceditor"></div>
            <textarea%(attrs)s>%(body)s</textarea>

            <script type="text/javascript">
                (function () {
                    var opts = {
                      container: '%(id)sepiceditor',
                      basePath: '%(basePath)s/epiceditor',
                      clientSideStorage: false,
                      useNativeFullsreen: true,
                      parser: marked,
                      //theme: {
                      //  base:'/themes/base/epiceditor.css',
                      //  preview:'/themes/preview/preview-dark.css',
                      //  editor:'/themes/editor/epic-dark.css'
                      //},
                      focusOnLoad: false,
                      shortcut: {
                        modifier: 18,
                        fullscreen: 70,
                        preview: 80
                      }
                    }
                    var editor = new EpicEditor(opts);

                    // be sure to populate the textarea
                    $textarea = $('#%(id)s');
                    editor.on('load', function (file) {
                      $textarea.val(file.content);
                    });
                    editor.on('update', function (file) {
                      $textarea.val(file.content);
                    });

                    // Everything is all setup, so load!
                    editor.load();
                })();
            </script>
            """ % {
                'basePath': settings.STATIC_URL,
                'attrs': flatatt(final_attrs),
                'body': conditional_escape(force_unicode(value)),
                'id': attrs['id'],
            }
        return mark_safe(html)


class AdminEpicEditorWidget(admin_widgets.AdminTextareaWidget, EpicEditorWidget):
    class Media:
        pass