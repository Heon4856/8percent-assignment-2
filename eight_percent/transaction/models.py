from django.db import models

from users.models import Users


class Account(models.Model):
    number = models.CharField(max_length=30)
    password = models.CharField(max_length=100)

    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    user = models.ForeignKey('users.Users', on_delete=models.CASCADE)

    class Meta:
        db_table = 'accounts'


class TransactionType(models.Model):
    type = models.CharField(max_length=15)

    class Meta:
        db_table = 'transaction_types'


class Transaction(models.Model):
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=50)
    counterparty = models.CharField(max_length=20)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    transaction_type = models.ForeignKey('TransactionType', on_delete=models.CASCADE)

    class Meta:
        db_table = 'transactions'
