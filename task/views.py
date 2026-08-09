from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Subquery, OuterRef
from django.urls import reverse_lazy
from task.forms import TaskForm, TodoStatusForm
from .models import *
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView, View
# Create your views here.

# Get a list of todos
@login_required
def index(request):

    status = TodoStatus.objects.filter(
        todo_id=OuterRef("id")
    ).order_by("-created_at")

    todos = Todo.objects.filter(
        created_by=request.user
    ).annotate(
        status=Subquery(status.values("status")[:1])
    )

    context = {
        "todos": todos
    }
    return render(request, "home.html", context)

# Gets one of the tasks
@login_required
def task_details(request, **kwargs):
    id = kwargs.get("id", None)

    if id is None:
        return redirect("task:home")

    obj = None
    try:
        status = TodoStatus.objects.filter(
            todo_id=OuterRef("id")
        ).order_by("-created_at")
        obj = Todo.objects.annotate(
            status=Subquery(status.values("status")[:1])
        ).get(id=id)
        
    except:
        obj = None

    statuses = TodoStatus.objects.filter(
        todo=obj
    )

    change_status_form = TodoStatusForm(data={"status": obj.status})

    context = {
        "todo": obj,
        "statuses": statuses,
        "form": change_status_form
    }

    return render(request, "details.html", context)

# create a todo
@login_required
def create_task(request):
    form = TaskForm()

    if request.method == "POST":
        
        form = TaskForm(request.POST)

        if form.is_valid():
            new_todo = Todo.objects.create(
                name=request.POST.get("name"),
                created_by=request.user
            )

            # pending status
            TodoStatus.objects.create(
                todo=new_todo,
                status="Pending"
            )
            messages.success(request, "Todo successfully created.")
            return redirect("task:home")

    context = {
        "form": form
    }

    return render(request, "create.html", context)

@login_required
def update_task(request, **kwargs):
    id = kwargs.get("id", None)
    
    if id is None:
        return redirect("task:home")

    obj = None
    try:
        obj = Todo.objects.get(id=id)
    except:
        obj = None

    if request.method == "POST":
        name = request.POST.get("name")
        obj.name = name
        obj.save()

    form = TaskForm({"name": obj.name})
    context = {
        "todo": obj,
        "form": form
    }
    return render(request, "update.html", context)

@login_required
def delete_task(request, **kwargs):
    id = kwargs.get("id")

    if id is None:
        return redirect("task:home")

    obj = None
    try:
        obj = Todo.objects.get(id=id)
    except:
        obj = None
            
    if request.method == "POST":
        obj.delete()
        return redirect("task:home")

    context = {
        "todo": obj
    }
    return render(request, "delete.html", context)

@login_required
def change_status(request, id):
    todo = get_object_or_404(Todo, id=id)

    if request.method != "POST":
        return redirect(reverse_lazy("task:details", kwargs={"id": id}))
        
    form = TodoStatusForm(request.POST)

    if not form.is_valid():
        messages.error(request, "This is something wrong with your input.")
        return redirect(reverse_lazy("task:details", kwargs={"id": id}))

    status = form.cleaned_data.get("status")
    print(status)
    try:
        current_status = TodoStatus.objects.filter(todo=todo).latest("created_at")
        print(current_status.status)
        if current_status.status == status:
            messages.error(request, "You have already selected this status as your current status. Please select another status")
            return redirect(reverse_lazy("task:details", kwargs={"id": id}))
    except Exception as e:
        print(e)
        pass

    TodoStatus.objects.create(
        todo=todo,
        status=status
    )
    messages.success(request, "Status updated successfully!")
    return redirect(reverse_lazy("task:details", kwargs={"id": id}))

# LoginRequiredMixin to check for authenticated users
class TodoList(LoginRequiredMixin, ListView):

    model = Todo
    template_name = "home.html"
    context_object_name = "todos"
    ordering = "-created_at"

class TodoDetails(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = "details.html"
    context_object_name = "todo"
    slug_url_kwarg = "id"


class CreateTodo(LoginRequiredMixin, CreateView):
    model = Todo
    form_class = TaskForm
    template_name = "create.html"
    success_url = "/"

    def form_valid(self, form):
        if form.is_valid():
            Todo.objects.create(
                name=form.cleaned_data.get("name"),
                created_by=self.request.user
            )

            return redirect("task:home")
        return super().form_valid(form)
    