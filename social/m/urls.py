from django.urls import path
from . import views


app_name = "m"
urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list', views.profile_list, name="profile_list"),
    path('profile/<int:pk>', views.profile, name="profile"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('register/', views.user_register, name="register"),
    path('update_user/', views.update_user, name="update_user"),
    path('tweet_like/<int:pk>', views.tweet_like, name="tweet_like"),
]
