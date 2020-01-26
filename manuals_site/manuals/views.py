import datetime

from django.utils import timezone
from django.shortcuts import render
from django.urls import reverse_lazy
from .my_functions import reverse_query, get_assignment_count
from .models import Manual, Directory
from .forms import (
    ManualForm,
    ManualAssignForm,
    ManualArchiveForm,
    ManualNextUpdateForm,
    DirectoryForm,
    DirectoryUpdateForm
)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def index(request):
    if request.method == 'GET':
        dir_id = int(request.GET.get('dir_id', default=1))
        current_folder = Directory.objects.get(pk=dir_id)

        children = current_folder.get_children()
        ancestors = current_folder.get_ancestors()
        manuals = current_folder.manuals(manager='active_objects').all()

        context = {
            'directories': children,
            'current_folder': current_folder,
            'ancestors': ancestors,
            'manuals': manuals,
        }

        if request.is_ajax():
            # The request is ajax; refresh the directory table.
            return render(request, 'manuals/index_table.html', context)
        else:
            # The request is not ajax; load the index page.
            # Add assignments count to context for info cue on header
            assignments = get_assignment_count(request.user)
            context.update(assignments)
            return render(request, 'manuals/index.html', context)


# add test so to check that user.is_staff
@login_required
def manage(request):
    current_user = request.user
    admin_of = current_user.admin_of(manager='active_objects').all()
    context = {'admin_of': admin_of}

    return render(request, 'manuals/manage.html', context)

@login_required
def assignments(request):
    current_user = request.user
    assigned = current_user.assigned_to(manager='active_objects').all()

    context = {'assigned': assigned}

    return render(request, 'manuals/assignments.html', context)


@login_required
def archive(request):
    archived = Manual.objects.filter(is_archived=True)
    context = {'archived': archived}

    return render(request, 'manuals/archive.html', context)


def search(request):
    # Right now search is very basic. Future improvements would be
    # to merge the different results querysets into one set
    # to make rendering in template more flexible.
    # Formatting the query string to make it more useful such as
    # removing stop words and handling singular/plural version of words.
    # Adding more fields such as author and update_status.

    if request.method == "GET":
        # Get the query string from the request
        qs = request.GET.get('qs')

        titles = Manual.objects.filter(title__icontains=qs)
        tags = Manual.objects.filter(tags__icontains=qs).exclude(id__in=titles)
        contents = Manual.objects.filter(content__icontains=qs).exclude(id__in=tags)

        results = {
            'titles': titles,
            'tags': tags,
            'contents': contents,
        }

    return render(request, 'manuals/search_results.html', results)


# ** Manual Views **

class ManualDetail(DetailView):
    model = Manual
    template_name = 'manuals/manual_detail.html'
    context_object_name = 'manual'    


class ManualCreate(LoginRequiredMixin, CreateView):
    form_class = ManualForm
    model = Manual
    # fields = ['title', 'content', 'folder', 'tags']
    template_name = 'manuals/manual_form.html'

    def get_form_kwargs(self):
        current_dir_id = int(self.request.GET.get('current_dir', default=1))
        kwargs = super(ManualCreate, self).get_form_kwargs()
        kwargs['current_dir'] = Directory.objects.get(pk=current_dir_id)
        return kwargs

    def form_valid(self, form):
        now = timezone.now()
        form.instance.author = self.request.user
        form.instance.last_update_by = self.request.user
        form.instance.next_update = now + datetime.timedelta(days=90)
        return super().form_valid(form)


class ManualUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = ManualForm
    model = Manual
    # fields = ['title', 'content', 'folder', 'tags']
    template_name = 'manuals/manual_form.html'

    def form_valid(self, form):
        now = timezone.now()
        form.instance.last_update_by = self.request.user
        form.instance.next_update = now + datetime.timedelta(days=90)
        return super().form_valid(form)
    
    # will likely need to change or get rid of this function so all users can edit
    def test_func(self):
        manual = self.get_object()
        if self.request.user == manual.author or self.request.user.is_staff:
            return True
        return False


class ManualDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Manual
    
    def test_func(self):
        manual = self.get_object()
        if self.request.user == manual.author:
            return True
        return False

    def get_success_url(self):
        return reverse_lazy('archive')


class ManualAssign(LoginRequiredMixin, BSModalUpdateView):
    form_class = ManualAssignForm
    model = Manual
    template_name = 'manuals/manual_manage_form.html'

    success_message = 'Manual updated successfully'
    success_url = reverse_lazy('manage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Assign user for next update'
        return context


class ManualNextUpdate(LoginRequiredMixin, BSModalUpdateView):
    form_class = ManualNextUpdateForm
    model = Manual
    template_name = 'manuals/manual_manage_form.html'

    success_message = 'Manual updated successfully'
    success_url = reverse_lazy('manage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Change next update'
        return context


class ManualArchive(LoginRequiredMixin, BSModalUpdateView):
    form_class = ManualArchiveForm
    model = Manual
    template_name = 'manuals/manual_manage_form.html'

    success_message = 'Manual has been archived successfully'
    success_url = reverse_lazy('manage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Archive this manual?'
        return context


class ManualRestore(LoginRequiredMixin, BSModalUpdateView):
    form_class = ManualArchiveForm
    model = Manual
    template_name = 'manuals/manual_manage_form.html'

    success_message = 'Manual has been restored successfully'
    success_url = reverse_lazy('archive')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Restore this manual?'
        return context


class ManualAdminDelete(LoginRequiredMixin, BSModalDeleteView):
    model = Manual
    template_name = 'manuals/manual_admin_confirm_delete.html'
    success_message = 'Manual deleted successfully'
    success_url = reverse_lazy('manage')


# ** Directory Views **

class DirectoryCreate(LoginRequiredMixin, BSModalCreateView):
    form_class = DirectoryForm
    model = Directory
    template_name = 'manuals/directory_form.html'

    success_message = 'Folder created successfully'

    def form_valid(self, form):
        dir_id = int(self.request.GET.get('dir_id', default=1))
        current_folder = Directory.objects.get(pk=dir_id)
        form.instance.parent = current_folder
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Folder'
        return context

    def get_success_url(self):
        dir_id = self.request.GET.get('dir_id', default=1)
        return reverse_query('index', get={'dir_id': dir_id})


class DirectoryUpdate(LoginRequiredMixin, BSModalUpdateView):
    form_class = DirectoryUpdateForm
    model = Directory
    template_name = 'manuals/directory_form.html'

    success_message = 'Folder saved successfully'

    # Will want to overide form_valid method to prevent users from create new root nodes.

    def get_form_kwargs(self):
        node_id = self.request.GET.get('node', default=1)
        kwargs = super(DirectoryUpdate, self).get_form_kwargs()
        kwargs['node'] = Directory.objects.get(pk=node_id)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Folder'
        return context

    def get_success_url(self):
        dir_id = self.request.GET.get('dir_id', default=1)
        return reverse_query('index', get={'dir_id': dir_id})


class DirectoryDelete(LoginRequiredMixin, BSModalDeleteView):
    model = Directory

    success_message = 'Folder deleted successfully'

    def get_success_url(self):
        dir_id = self.request.GET.get('dir_id', default=1)
        return reverse_query('index', get={'dir_id': dir_id})