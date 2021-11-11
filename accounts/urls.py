from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import register_view, login_view

urlpatterns = [
    path("register/", register_view, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", login_view, name="login"),
]
