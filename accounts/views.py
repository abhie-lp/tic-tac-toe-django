from typing import Optional

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from .models import CustomUser
from .forms import RegisterForm, LoginForm


def login_view(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            auth_user: Optional[CustomUser] = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if auth_user and auth_user.is_active:
                login(request, auth_user)
                return redirect("/")
            form.add_error(None, "Username or Password is invalid")
    return render(request, "accounts/login.html", {"form": form})


def register_view(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user: CustomUser = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("/")
    return render(request, "accounts/register.html", {"form": form})
