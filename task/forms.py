from django import forms
from . models import Todo, TodoStatus

class TaskForm(forms.ModelForm):

    class Meta:
        fields = ["name",]
        model = Todo

class TodoStatusForm(forms.Form):
    status = forms.ChoiceField(
        choices=[
            ("", "Change Status"),
            ("Pending", "Pending"), 
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled")
        ],
        required=True,
        label="Statuses"
    )

    class Meta:
        fields = ["status",]