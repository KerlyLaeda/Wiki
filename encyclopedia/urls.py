from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    # search
    path("add/", views.add, name="add"),
    path("edit/<str:title>/", views.edit, name="edit"),
    path("random/", views.random_page, name="random")
]
