import architect
from django.db import models
from django.utils import timezone

from ..users.models import Users


class Account(models.Model):
    number = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    balance = models.PositiveBigIntegerField(default=0)
    user = models.ForeignKey(Users, on_delete=models.PROTECT)

    class Meta:
        db_table = 'accounts'


class TransactionType(models.Model):
    class TransactionTypeEnum(models.IntegerChoices):
        DEPOSIT = 1
        WITHDRAW = 2

    type = models.PositiveSmallIntegerField(choices=TransactionTypeEnum.choices)

    class Meta:
        db_table = 'transaction_types'


@architect.install('partition', type='range', subtype='date', constraint='month', column='created_at')
class Transaction(models.Model):
    amount = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=7)
    counterparty = models.CharField(max_length=10)
    balance = models.BigIntegerField(default=0)
    account = models.CharField(max_length=30)
    transaction_type = models.IntegerField()

    class Meta:
        db_table = 'transactions'
        indexes = [
            models.Index(fields=['transaction_type', ]),
            models.Index(fields=['account', ]),

        ]
