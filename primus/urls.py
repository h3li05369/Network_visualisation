from django.urls import path
from . import views



urlpatterns = [
    path('',views.homepage, name="home"),
    path('edit_favorites',views.edit_favorites, name="edit_favorite")
]
