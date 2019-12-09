from django.shortcuts import render
from django.urls import reverse_lazy
from .my_functions import reverse_query
from .models import Manual, Directory
from .forms import ManualForm, DirectoryForm, DirectoryUpdateForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def index(request):
    if request.method == 'GET':
        dir_id = int(request.GET.get('dir_id', default=1))
        current_folder = Directory.objects.get(pk=dir_id)

        children = current_folder.get_children()
        ancestors = current_folder.get_ancestors()
        manuals = current_folder.manuals.all()

        directories = {
            'directories': children,
            'current_folder': current_folder,
            'ancestors': ancestors,
            'manuals': manuals,
        }

        if request.is_ajax():
            # The request is ajax; refresh the directory table.
            return render(request, 'manuals/index_ajax.html', directories)
        else:
            # The request is not ajax; load the index page.
            return render(request, 'manuals/index.html', directories)

class ManualDetail(DetailView):
    model = Manual
    template_name = 'manuals/manual_detail.html'
    context_object_name = 'manual'    

class ManualCreate(LoginRequiredMixin, CreateView):
    form_class = ManualForm
    model = Manual
    # fields = ['title', 'content', 'folder', 'tags']
    template_name = 'manuals/manual_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ManualUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = ManualForm
    model = Manual
    # fields = ['title', 'content', 'folder', 'tags']
    template_name = 'manuals/manual_form.html'

    #Figure out a way to make a separate field for last_updated_by User
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        manual = self.get_object()
        if self.request.user == manual.author:
            return True
        return False

class ManualDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Manual
    success_url = '/'
    
    def test_func(self):
        manual = self.get_object()
        if self.request.user == manual.author:
            return True
        return False

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