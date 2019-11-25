from django.forms import ModelForm
from .models import Manual
from tinymce.widgets import TinyMCE

class ManualForm(ModelForm):
    class Meta:
        model = Manual
        fields = ['title', 'content', 'folder', 'tags']
        widgets = {
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30})
        }