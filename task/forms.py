from django import forms
from . models import Todo, TodoStatus

class TaskForm(forms.ModelForm):
    
    class Meta:
        fields = ["name",]
        model = Todo
        widgets = {
            "name": forms.Textarea(
                attrs={
                    "required": True,
                    "rows": 3,
                    "placeholder": "What are you doing today?"
                }
            )
        }
        labels = {
            "name": ""
        }

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