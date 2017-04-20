""" Having a TextField with json encoded data in it, this widget shows a human friendly
     key-value representation of the data below the textarea. This view is read-only and
     modifications are done in the default textarea.
"""
import json

from django import forms
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class JSONTextWidget(forms.widgets.Textarea):
    def render(self, name, value, attrs=None, **kwargs):
        if value is None:
            value = ''
        # noinspection PyBroadException
        try:
            # Django <=1.10
            # noinspection PyArgumentList
            final_attrs = self.build_attrs(attrs, name=name)
        except:
            # Django 1.11+
            attrs.setdefault('name', name)
            final_attrs = self.build_attrs(attrs)
        html = mark_safe('<div style="direction: ltr; text-align: left;">')

        try:
            json_decode = json.loads('{' + (value or '') + '}')
        except ValueError:
            json_decode = {'ERROR': 'failed to parse string as json'}
        for k in sorted(json_decode.keys()):
            html += format_html('<b>{}:</b> <code>{}</code><br/>', force_text(k), force_text(json_decode[k]))
        html += format_html('<br/><textarea style="width: 98%;" {}>\r\n{}</textarea>', flatatt(final_attrs), force_text(value))
        html += mark_safe('</div>')
        return html
    
