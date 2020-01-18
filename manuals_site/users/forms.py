from django import forms
from django.forms import ModelForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from bootstrap_modal_forms.forms import BSModalForm

from manuals.models import Directory, Manual
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]


# This exists in case there's a future possibility that user fields
# Path to this form can be turned on/off in Settings
class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']


class ProfileChangeImageForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class AddFavoriteForm(BSModalForm):
    class Meta:
        model = Profile
        fields = ['directory_favorites']

    def __init__(self, *args, **kwargs):
        favs = kwargs.pop('favs', None)
        super(AddFavoriteForm, self).__init__(*args, **kwargs)
        self.initial['directory_favorites'] = None

    def save(self, *args, **kwargs):
        print(favs)
        self.directory_favorites = favs
        super(AddFavoriteForm, self).save(*args, **kwargs)

