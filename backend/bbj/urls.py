from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login),
    path("register", views.register),
    path("checkLoginState", views.checkLoginState),
    path("logout", views.logout),
]
