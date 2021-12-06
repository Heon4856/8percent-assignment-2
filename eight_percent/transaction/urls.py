from django.urls import path

from .views import CreateAccountView, TransactionHistoryView, TransactionView, AccountViewSet

urlpatterns = [
    path('/history', TransactionHistoryView.as_view()),
    path('/create_account', CreateAccountView.as_view()),
    path('/lookup_account', AccountViewSet.as_view({'get': 'list'})),
    path('/transaction', TransactionView.as_view())
]