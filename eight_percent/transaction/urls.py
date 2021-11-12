from django.urls import path

from .views import CreateAccountView, LookupAccountView, Transaction

urlpatterns = [
    path('/Transaction', Transaction.as_view()),
    path('/create_account', CreateAccountView.as_view()),
    path('/lookup_account', LookupAccountView.as_view()),
]