from django.forms import ModelForm
from bootstrap_modal_forms.forms import BSModalForm
from mptt.forms import TreeNodeChoiceField
from .models import Manual, Directory
from .my_functions import valid_move_nodes
from tinymce.widgets import TinyMCE

class ManualForm(ModelForm):
    class Meta:
        model = Manual
        fields = ['title', 'content', 'folder', 'tags']
        widgets = {
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30})
        }
    
    def __init__(self, *args, **kwargs):
        # Get current directory to set initial parent when creating new manuals
        # Use set parent when updating manuals
        current_dir = kwargs.pop('current_dir', None)
        if current_dir:
            super(ManualForm, self).__init__(*args, **kwargs)
            self.initial['folder'] = current_dir
        else:
            super(ManualForm, self).__init__(*args, **kwargs)

class DirectoryForm(BSModalForm):
    class Meta:
        model = Directory
        fields = ['name']

class DirectoryUpdateForm(DirectoryForm):
    class Meta(DirectoryForm.Meta):
        fields = ['name', 'parent']

    def __init__(self, node, *args, **kwargs):
        # Populate Parent selector with only nodes that are valid targets to move to
        super(DirectoryForm, self).__init__(*args, **kwargs)
        self.fields['parent'] = TreeNodeChoiceField(valid_move_nodes(node))

class ManualAssignForm(BSModalForm):
    class Meta:
        model = Manual
        fields = ['update_assigned_to']

class ManualNextUpdateForm(BSModalForm):
    class Meta:
        model = Manual
        fields = ['next_update']

class ManualArchiveForm(BSModalForm):
    class Meta:
        model = Manual
        fields = ['is_archived']