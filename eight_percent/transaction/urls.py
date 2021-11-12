from django.urls import path

from .views import CreateAccountView, LookupAccountView, TransactionHistoryView, TransactionView

urlpatterns = [
    path('/history', TransactionHistoryView.as_view()),
    path('/create_account', CreateAccountView.as_view()),
    path('/lookup_account', LookupAccountView.as_view()),
    path('/transaction', TransactionView.as_view())
]