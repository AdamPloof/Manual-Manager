from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from bootstrap_modal_forms.generic import BSModalUpdateView

from .forms import UserRegisterForm, AddFavoriteForm
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
def profile_add_fav(request):
    # Add selected file or folder to user's profile's favorites list
    
    if request.method == "POST":
        user = request.user
        current_favs = user.profile.directory_favorites.all()

        new_fav_id = int(request.POST.get('add_fav'))
        new_fav = Directory.objects.filter(pk=new_fav_id)

        favs_list = current_favs | new_fav

        user.profile.directory_favorites.set(favs_list)

        messages.success(request, f'Added {new_fav[0].name} to favorites!')

        # Append the current folder id as search query to the redirect url
        dir_id = request.GET.get('dir_id')
        redirect_url = reverse_query('index', get={'dir_id': dir_id})

        return redirect(redirect_url)

    else:
        messages.error(request, 'The favorite requested is invalid' )

        # Append the current folder id as search query to the redirect url
        current_dir_id = request.GET.get('dir_id')
        redirect_url = reverse_query('index', get={'dir_id': dir_id})

        return redirect(redirect_url)


# class ProfileAddFavFolder(LoginRequiredMixin, BSModalUpdateView):
#     model = Profile
#     form_class = AddFavoriteForm
#     template_name = 'users/favorites_form.html'
#     success_message = "Folder was added to your favorites"

#     def get_form_kwargs(self):
#         # Retrieve all the current favorites for folders for the current user

#         user = self.request.user
#         current_favs = user.profile.directory_favorites.all()
#         new_fav_id = self.request.GET.get('node')
#         new_fav = Directory.objects.filter(pk=new_fav_id)
#         new_favs_list = current_favs | new_fav

#         kwargs = super(ProfileAddFavFolder, self).get_form_kwargs()
#         kwargs['favs'] = new_favs_list
#         return kwargs

#     def get_context_data(self, **kwargs):
#         new_fav_id = self.request.GET.get('node')
#         new_fav = Directory.objects.get(pk=new_fav_id)
#         context = super().get_context_data(**kwargs)
#         context['new_fav'] = new_fav
#         context['title'] = 'Add Favorite'
#         return context

#     def get_success_url(self):
#         dir_id = self.request.GET.get('dir_id', default=1)
#         return reverse_query('index', get={'dir_id': dir_id})