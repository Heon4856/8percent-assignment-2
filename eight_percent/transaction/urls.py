from django.urls import path

from .views import   TransactionView, AccountViewSet

urlpatterns = [
    path('/account', AccountViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('', TransactionView.as_view({'get': 'list', 'post': 'create'}))
]