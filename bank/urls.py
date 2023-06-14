from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("",views.loginuser, name="login"),
    path("dashboard", views.user_dashboard, name="dashboard"),
    path("logout", views.logoutuser, name="logout"),
    path("signup", views.signup, name="signup"),
    path("withdraw", views.withdraw, name="withdraw"),
    path("analytics", views.analytics, name="analytics"),
    path("transfer",views.transfer_fund, name="transfer"),
    path("user",views.user, name="user"),
    path("changePassword",views.chnage_password, name="user"),
]
