from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required

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

# add test so to check that user.is_staff
@login_required
def manage(request):
    return render(request, 'users/manage.html')
 