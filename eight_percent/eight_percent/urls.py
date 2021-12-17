from django.urls import include, path

urlpatterns = [
    path('users', include('users.urls')),
    path('transaction', include('transaction.urls')),

]
