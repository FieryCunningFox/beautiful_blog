from django.urls import path
from .views_api import loginView, registerView

urlpatterns = [
    path("login/", loginView.as_view()),
    path("register/", registerView.as_view()),
]
