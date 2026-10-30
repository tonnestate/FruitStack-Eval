"""Issue example of django__django-11019 (merging 3+ form Media objects must not warn and must keep the pairwise orders).
usage: PYTHONPATH=<django tree> python repro_issue_example.py      exit 0 = issue behaviour fixed (no MediaOrderConflictWarning, order text-editor < text-editor-extras < color-picker)."""
import sys
import warnings

import django
from django import forms
from django.conf import settings

settings.configure()
django.setup()


class ColorPicker(forms.Widget):
    class Media:
        js = ['color-picker.js']


class SimpleTextWidget(forms.Widget):
    class Media:
        js = ['text-editor.js']


class FancyTextWidget(forms.Widget):
    class Media:
        js = ['text-editor.js', 'text-editor-extras.js', 'color-picker.js']


class MyForm(forms.Form):
    background_color = forms.CharField(widget=ColorPicker())
    intro = forms.CharField(widget=SimpleTextWidget())
    body = forms.CharField(widget=FancyTextWidget())


with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    js = MyForm().media._js
js_list = list(js)
print("django from:", django.__file__)
print("merged js:", js_list)
print("warnings:", [str(w.message)[:80] for w in caught])
ok = not caught and js_list.index("text-editor.js") < js_list.index("text-editor-extras.js") < js_list.index("color-picker.js")
print("ISSUE_BEHAVIOUR_FIXED" if ok else "ISSUE_BEHAVIOUR_PRESENT")
sys.exit(0 if ok else 1)
