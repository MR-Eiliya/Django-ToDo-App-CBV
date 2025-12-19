from django import forms
from .models import Task


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Update task..."}
            )
        }
