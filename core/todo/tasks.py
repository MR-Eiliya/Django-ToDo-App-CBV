from celery import shared_task
from .models import Task

@shared_task
def delete_completed_tasks():
    deleted_count, _ = Task.objects.filter(is_completed=True).delete()
    return deleted_count