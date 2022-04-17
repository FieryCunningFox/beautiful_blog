from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('contact/', contact, name="contact"),
    path('posts/', posts, name="posts"),
    path('register/', register, name="register"),
    path('login/', LoginView.as_view(), name="login")
]
