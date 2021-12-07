from django.urls import path

from .views import  TransactionHistoryView, TransactionView, AccountViewSet

urlpatterns = [
    path('/history', TransactionHistoryView.as_view()),
    path('/account', AccountViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('/transaction', TransactionView.as_view({'post':'create'}))
]