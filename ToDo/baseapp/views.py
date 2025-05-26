from django.shortcuts import render,HttpResponse,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.
class CustomLogin(LoginView):
    fields = '__all__'
    template_name = 'login.html'
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('TaskList')
    
class Register(FormView):
    template_name = 'register.html'
    success_url = reverse_lazy('TaskList')
    redirect_authenticated_user = True
    form_class = UserCreationForm
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(Register,self).form_valid(form)
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('TaskList')
        return super(Register,self).get(request, *args, **kwargs)

class TaskList(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(user=self.request.user)  # Fetch fresh data
        context['count'] = context['tasks'].filter(completed=False).count()

        search_input = self.request.GET.get('search-key') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(task__icontains=search_input)
        context['search_input'] = search_input
        return context

    
class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'

class CreateTask(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['task','description','completed']
    success_url = reverse_lazy('TaskList')
    template_name = 'create_task.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask,self).form_valid(form)

class UpdateTask(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['task','description','completed']
    success_url = reverse_lazy('TaskList')
    template_name = 'create_task.html'

class DeleteTask(LoginRequiredMixin,DeleteView):
    model = Task
    success_url = reverse_lazy('TaskList')
    context_object_name = 'task'
    template_name = 'delete_task.html'