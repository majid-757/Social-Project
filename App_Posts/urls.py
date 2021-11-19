from django.urls import path

from .views import home, liked, unliked

app_name = 'App_Posts'

urlpatterns = [
    path("", home, name="home"),
    path("liked/<pk>/", liked, name="liked"),
    path("unliked/<pk>/", unliked, name="unliked"),
]











