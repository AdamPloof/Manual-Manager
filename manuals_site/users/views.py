
from django.shortcuts import (
    render,
    reverse,
    redirect,
    get_object_or_404,
)

from django.contrib.auth.models import User

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView
from bootstrap_modal_forms.generic import BSModalUpdateView

from .forms import (
    UserRegisterForm,
    AddFavoriteForm,
    ProfileChangeImageForm,
    UserUpdateForm
)

from .models import Profile

from manuals.models import Directory, Manual
from manuals.my_functions import reverse_query


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    current_user = request.user
    author = current_user.author.all()
    assigned = current_user.assigned_to.all()
    admin_of = current_user.admin_of.all()
    updated_by = current_user.updated_by.all()

    context = {
        'author': author,
        'assigned': assigned,
        'admin_of': admin_of,
        'updated': updated_by
    }

    return render(request, 'users/profile.html', context)


@login_required
def preferences(request):
    user = request.user

    return render(request, 'users/preferences.html')


@login_required
def manage_favs(request):
    user = request.user
    dir_favs = user.profile.directory_favorites.all()
    man_favs = user.profile.manual_favorites.all()

    context = {
        'dir_favs': dir_favs,
        'man_favs': man_favs
        }

    return render(request, 'users/favorites.html', context)


@login_required
def profile_add_fav(request):
    # Add selected file or folder to user's profile's favorites list
    
    if request.method == "POST":
        user = request.user
        fav_type = request.POST.get('fav_type')
        fav_id = int(request.POST.get('fav_id'))

        # Check if favorite is a directory
        if fav_type == 'folder':

            # Check if directory is already in user's favorites
            if not user.profile.directory_favorites.filter(pk=fav_id).exists():
                new_fav = Directory.objects.filter(pk=fav_id)
                current_favs = user.profile.directory_favorites.all()
                favs_list = current_favs | new_fav
                user.profile.directory_favorites.set(favs_list)
                messages.success(request, f'Added {new_fav[0].name} to favorites!')
            else:
                messages.error(request, 'The selected folder is already in favorites', extra_tags='warning')

        # Check if favorite is a manual
        elif fav_type == 'file':

            # Check if manual is already in user's favorites
            if not user.profile.manual_favorites.filter(pk=fav_id).exists():
                new_fav = Manual.objects.filter(pk=fav_id)
                current_favs = user.profile.manual_favorites.all()
                favs_list = current_favs | new_fav
                user.profile.manual_favorites.set(favs_list)
                messages.success(request, f'Added {new_fav[0].title} to favorites!')
            else:
                messages.error(request, 'The selected manual is already in favorites', extra_tags='warning')
        
        # Favorite is neither manual or directory
        else:
            messages.error(request, 'The favorite requested is invalid', extra_tags='danger')

    # Request is not a POST request      
    else:
        messages.error(request, 'The favorite requested is invalid', extra_tags='danger')

    # Append the current folder id as search query to the redirect url
    dir_id = request.GET.get('dir_id')
    redirect_url = reverse_query('index', get={'dir_id': dir_id})

    return redirect(redirect_url)


@login_required
def profile_remove_fav(request):
    # Remove selected file or folder to user's profile's favorites list
    
    if request.method == "POST":
        user = request.user
        fav_type = request.POST.get('fav_type')
        fav_id = int(request.POST.get('fav_id'))

        # Check if favorite is a directory
        if fav_type == 'folder':

            # Check if directory is already in user's favorites
            if user.profile.directory_favorites.filter(pk=fav_id).exists():
                this_fav = Directory.objects.get(pk=fav_id)
                user.profile.directory_favorites.remove(this_fav)
                messages.success(request, f'{this_fav.name} has been removed from favorites!')
            else:
                messages.error(request, 'The selected folder is not in favorites', extra_tags='warning')

        # Check if favorite is a manual
        elif fav_type == 'file':

            # Check if manual is already in user's favorites
            if user.profile.manual_favorites.filter(pk=fav_id).exists():
                this_fav = Manual.objects.get(pk=fav_id)
                user.profile.manual_favorites.remove(this_fav)
                messages.success(request, f'{this_fav.title} has been removed from favorites!')
            else:
                messages.error(request, 'The selected manual is not in favorites', extra_tags='warning')
        
        # Favorite is neither manual or directory
        else:
            messages.error(request, 'The favorite requested is invalid', extra_tags='danger')

    # Request is not a POST request      
    else:
        messages.error(request, 'The favorite requested is invalid', extra_tags='danger')

    return redirect('favorites')


# This exists in case there's a future possibility that user fields
# Path to this form can be turned on/off in Settings
class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = UserUpdateForm
    model = User
    template_name = 'users/user_update.html'

    def get_success_url(self):
        return reverse('preferences')

    def test_func(self):
        user = self.request.user
        self.object = self.get_object()

        if user == self.object:
            return True
        else:
            return False


class ProfileUpdateImageView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = ProfileChangeImageForm
    model = Profile
    template_name = 'users/profile_change_image.html'

    def get_success_url(self):
        return reverse('preferences')

    def test_func(self):
        user_profile = self.request.user.profile
        self.object = self.get_object()

        if user_profile == self.object:
            return True
        else:
            return False