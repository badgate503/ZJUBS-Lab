from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login),
    path("register", views.register),
    path("checkLoginState", views.checkLoginState),
    path("logout", views.logout),
    path("send_email", views.send_email),
    path("fetchItem", views.fetchItem),
    path("favorKey", views.favorKey),
    path("get_keyword_info", views.get_keyword_info),
    path("remove_favor", views.remove_favor),
    path("favor_notify", views.favorNotify),
    path("get_price_change", views.getPriceChange),
    path("tb_get_qrcode", views.tb_get_qrcode),
    path("close_driver", views.shut_driver),
    path("tb_get_cookie", views.tb_cookie),
    path("jd_get_qrcode", views.jd_get_qrcode),
    path("jd_get_cookie", views.jd_cookie)
]
