from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from games.views import game_page

urlpatterns = [
    path("game/", include("games.urls")),
    path('admin/', admin.site.urls),
    path("account/", include("accounts.urls")),
    path("", game_page, name="game_page"),
]

if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
