from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "is_completed", "created_date", "updated_date")
    list_filter = ("is_completed", "created_date", "updated_date")
    search_fields = ("title", "user__email", "user__username")


admin.site.register(Task, TaskAdmin)
