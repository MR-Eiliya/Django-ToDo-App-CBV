from django.urls import path, include
from .views import TaskListView, TaskCreateView, TaskUpdateView, TaskCompleteView, TaskDeleteView

app_name = "todo"

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('update/<int:pk>/', TaskUpdateView.as_view(), name='task_update'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='task_delete'),
    path('complete/<int:pk>/', TaskCompleteView.as_view(), name='task_complete'),
    path('api/v1/', include('todo.api.v1.urls')),
]