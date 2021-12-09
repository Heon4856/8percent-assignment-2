import datetime

import architect
from django.db import models
from django.utils import timezone
from users.models import Users


class Account(models.Model):
    number = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    class Meta:
        db_table = 'accounts'


class TransactionType(models.Model):
    class TransactionTypeChoice(models.IntegerChoices):
        DEPOSIT = 1
        WITHDRAW = 2

    type = models.PositiveSmallIntegerField(choices=TransactionTypeChoice.choices)

    class Meta:
        db_table = 'transaction_types'


@architect.install('partition', type='range', subtype='date', constraint='month', column='created_at')
class Transaction(models.Model):
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=50)
    counterparty = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    transaction_type = models.ForeignKey('TransactionType', on_delete=models.CASCADE)

    class Meta:
        db_table = 'transactions'
        indexes = [
            models.Index(fields=['created_at', ]),
            models.Index(fields=['account', ]),
            models.Index(fields=['transaction_type', ])
        ]
