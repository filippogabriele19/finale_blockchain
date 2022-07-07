from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", home_view, name="home"),
    path("signup/", signup_view, name="signup"),
    path("profile/", profile_view, name="profile"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="home.html"),
        name="logout",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path("do_offer/", do_new_offer, name="do_offer"),
]
