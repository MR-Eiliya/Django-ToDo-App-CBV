from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import TaskUpdateForm
from django.views import View
from django.contrib import messages

# cbv for showing the task list
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name =  'todo/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-created_date')
    
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        if title:
            Task.objects.create(user=request.user, title=title)
        return redirect('todo:task_list')
    

# cbv for task creation
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title"]
    template_name = 'todo/task_list.html'
    success_url = reverse_lazy('todo:task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

# cbv for task updating
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = 'todo/task_update.html'
    success_url = reverse_lazy('todo:task_list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    

# cbv for task complement
class TaskCompleteView(LoginRequiredMixin, View):
    model = Task
    success_url = reverse_lazy('todo:task_list')

    def get(self, request, *args, **kwargs):
        object = Task.objects.get(id=kwargs.get("pk"))
        object.is_completed = not object.is_completed
        object.save()
        return redirect(self.success_url)
    

# cbv for task deleting
class TaskDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = get_object_or_404(Task, id=pk, user=request.user)
        task.delete()
        messages.success(request,"Task has deleted successfully!")
        return redirect('todo:task_list')
    



    



