from django.urls import path
from . import views


app_name = "m"
urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list', views.profile_list, name="profile_list"),
]
