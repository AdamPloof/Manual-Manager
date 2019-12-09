from django.forms import ModelForm
from bootstrap_modal_forms.forms import BSModalForm
from .models import Manual, Directory
from tinymce.widgets import TinyMCE

class ManualForm(ModelForm):
    class Meta:
        model = Manual
        fields = ['title', 'content', 'folder', 'tags']
        widgets = {
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30})
        }

class DirectoryForm(BSModalForm):
    class Meta:
        model = Directory
        fields = ['name']

class DirectoryUpdateForm(DirectoryForm):
    class Meta(DirectoryForm.Meta):
        fields = ['name', 'parent']