from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from user.forms import CreateUserForm

# Create your views here.

def user_login(request):

    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("task:home")
    context = {
        "form": form
    }
    return render(request, "user/login.html", context)


@login_required
def user_logout(request):
    logout(request)

    return redirect("user:login")


def signup(request):

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully!. Please login with your new account.")
            return redirect("user:login")

    context = {
        "form": form
    }

    return render(request, "user/signup.html", context)