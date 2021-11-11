from django.contrib import admin
from django.urls import path, include
from games.views import game_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path("account/", include("accounts.urls")),
    path("", game_page, name="game_page"),
]
