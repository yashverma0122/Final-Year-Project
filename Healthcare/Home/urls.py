from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = "Home"

urlpatterns = [
    path("", views.homeview, name='Home'),
    path("member", views.member, name='BecomeAMember'),
    path("member/success", views.success, name='Success')
]