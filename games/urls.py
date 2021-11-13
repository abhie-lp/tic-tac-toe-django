from django.urls import path
from .views import change_symbol

urlpatterns = [
    path("change-symbol/", change_symbol, name="change_symbol"),
]
