from django.urls import path

from .views import SignInView, SignUpView

urlpatterns = [
    path('/login', SignInView.as_view()),
    path('/signup', SignUpView.as_view()),
]