from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import TaskUpdateForm
from django.views import View
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse


# cbv for showing the task list
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "todo/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by("-created_date")

    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")
        if title:
            Task.objects.create(user=request.user, title=title)
        return redirect("todo:task_list")


# cbv for task creation
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title"]
    template_name = "todo/task_list.html"
    success_url = reverse_lazy("todo:task_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# cbv for task updating
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = "todo/task_update.html"
    success_url = reverse_lazy("todo:task_list")

    def get_object(self, queryset=None):
        try:
            obj = self.model.objects.get(pk=self.kwargs["pk"])
        except self.model.DoesNotExist:
            raise PermissionDenied

        if obj.user != self.request.user:
            raise PermissionDenied

        return obj


# cbv for task complement
class TaskCompleteView(LoginRequiredMixin, View):
    model = Task
    success_url = reverse_lazy("todo:task_list")

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")

        try:
            task = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise PermissionDenied

        if task.user != request.user:
            raise PermissionDenied

        task.is_completed = not task.is_completed
        task.save()
        return redirect(self.success_url)


# cbv for task deleting
class TaskDeleteView(LoginRequiredMixin, View):
    success_url = reverse_lazy("todo:task_list")

    def get(self, request, pk):
        task = Task.objects.filter(pk=pk, user=request.user).first()
        if not task:
            return HttpResponse("403 Forbidden", status=403)

        task.delete()
        messages.success(request, "Task has been deleted successfully!")
        return redirect(self.success_url)
