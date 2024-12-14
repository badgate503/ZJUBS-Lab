from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login),
    path("register", views.register),
    path("checkLoginState", views.checkLoginState),
    path("logout", views.logout),
    path("send_email", views.send_email),
    path("tb_fetchItem", views.tb_fetchItem),
    path("db_fetchItem", views.db_fetchItem),
    path("tb_get_qrcode", views.tb_get_qrcode),
    path("close_driver", views.shut_driver),
    path("tb_get_cookie", views.tb_cookie)
]
