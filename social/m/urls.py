from django.urls import path
from . import views


app_name = "m"
urlpatterns = [
    path('', views.home, name="home"),
]
