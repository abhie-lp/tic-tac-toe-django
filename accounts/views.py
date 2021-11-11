from django.shortcuts import render, redirect
from django.contrib.auth import login

from .models import CustomUser
from .forms import RegisterForm


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
