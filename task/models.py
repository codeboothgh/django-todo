from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, related_name="todos", on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = "todo"
        verbose_name = "Todo"
        verbose_name_plural = 'Todos'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class TodoStatus(models.Model):
    todo = models.ForeignKey(
        Todo,
        related_name="todo_statuses",
        on_delete=models.CASCADE
    )
    status = models.CharField(max_length=100, default="Pending", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "todo_status"
        verbose_name = "Todo Status"
        verbose_name_plural = "Todo Statuses"
        ordering = ['-created_at']
        # get_latest_by = ['-created_at']

    def __str__(self):
        return self.todo.name + " - " + self.status


