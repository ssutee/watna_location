from django import forms
from django.forms import widgets
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

STATIC_URL_BASE = settings.STATIC_URL

class JSColorColorPicker(forms.TextInput):
    """
    Based on JSColor - http://jscolor.com
    Note:  Requires input to use class 'color'
    """
    class Media:
        js = (STATIC_URL_BASE + 'jscolor/jscolor.js',)

    def render(self, name, value, attrs=None):
        if not 'id' in attrs:
            attrs['id'] = "id_%s" % name

        if 'class' in attrs:
            attrs['class'] = attrs['class'] + ' color'
        else:
            attrs['class'] = 'color'

        return super(JSColorColorPicker, self).render(name, value, attrs)

class FlexiColorPicker(forms.TextInput):
    """
    Based on http://www.daviddurman.com/flexi-color-picker/
    """
    class Media:
        css = {'all': (STATIC_URL_BASE + 'flexi/themes.css',)}
        js = (STATIC_URL_BASE + 'flexi/colorpicker.min.js',)

    def _render_js(self, input_id, name, value):
        js = u"""
<script type="text/javascript">
    ColorPicker(
        document.getElementById('%s-slide'),
        document.getElementById('%s-picker'),
        function(hex, hsv, rgb) {
            input = document.getElementById('%s');
            input.value = hex;
            input.style.backgroundColor = hex;
        });
</script>""" % (name, name, input_id)
        return js

    def _render_html(self, name, value, attrs=None):
        rendered_input = super(FlexiColorPicker, self).render(name, value, attrs)
        picker_id = name + '-picker'
        slide_id = name + '-slide'
        html = """
            %s
            <div id="color-picker" class="cp-default">
                <div id="%s" class="picker-wrapper"></div>
                <div id="%s" class="slide-wrapper"></div>
            </div>
        """ % (rendered_input, picker_id, slide_id)
        return html

    def _render_css(self, name):
        """
        This is a hack.
        No default style is given so this is a temporary default setting...
        """
        css = """
<style type="text/css">
    #%s-picker { width: 200px; height: 200px }
    #%s-slide { width: 30px; height: 200px }
</style>""" % (name, name)
        return css

    def render(self, name, value, attrs=None):
        if not 'id' in attrs:
            attrs['id'] = "id_%s" % name
        return mark_safe(self._render_html(name, value, attrs) +
                         self._render_js(attrs['id'], name, value) + 
                         self._render_css(name))