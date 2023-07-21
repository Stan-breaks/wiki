from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new",views.create, name="new"),
    path("random",views.random_page,name="random"),
    path("entry/<str:title>", views.title,name="title"),
    path("edit/<str:title>",views.edit,name="edit") 
]
