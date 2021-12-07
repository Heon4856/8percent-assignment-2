import bcrypt
from django.db import transaction
from rest_framework.fields import CharField, IntegerField, DateField
from rest_framework.serializers import ModelSerializer, Serializer, Field

from .exceptions import BadRequestException
from .models import Account, Transaction


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ['password', 'number', 'balance', 'user']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['number', 'balance', 'user']

    def validate(self, data):
        password = data.get('password')

        if password is None:
            raise BadRequestException('name or number')

        return data



class TransactionSerializer(Serializer):
    amount = IntegerField()
    counterparty = CharField()
    account_number = CharField()
    account_password = CharField()
    transaction_type = IntegerField()
    description = CharField()


    def validate(self, data):
        if not data["account_number"]:
            raise BadRequestException({'message': 'ENTER_YOUR_ACCOUNT_NUMBER'})
        if not data["amount"]:
            raise BadRequestException({'message': 'ENTER_YOUR_AMOUNT'})
        if data["amount"] < 1:
            raise BadRequestException({'message': '알맞은 숫자의 amount를 입력하세요.'})
        if not data["counterparty"]:
            raise BadRequestException({'message': 'ENTER_YOUR_COUNTERPARTY'})
        if not data["account_password"]:
            raise BadRequestException({'message': 'INVALID_YOUR_ACCOUNT_NUMBER'})
        return data

    def create(self, validated_data):
       account = Account.objects.select_for_update().get(number=validated_data['account_number'])

       if not bcrypt.checkpw(validated_data['account_password'].encode('utf-8'),account.password.encode('utf-8')):
           raise BadRequestException({'message': '잘못된 비밀번호입니다.'})

       with transaction.atomic():
           if validated_data["transaction_type"] == 1:
               account.balance += validated_data["amount"]
           if validated_data["transaction_type"] == 2:
               account.balance -= validated_data["amount"]
           account.save()
           return Transaction.objects.create( amount=validated_data["amount"],
               description=validated_data["description"],
               counterparty=validated_data["counterparty"],
               account_id=account.id,
               transaction_type_id=validated_data["transaction_type"],
               balance=account.balance)

class TransactionModelSerializer(ModelSerializer):
    account_number = CharField(source='account.number')

    class Meta:
        model = Transaction
        fields = ["account_number", "amount", "created_at", "description", "counterparty", "balance", "transaction_type"]




class TransactionListSerializer(Serializer):
    account_number = CharField()
    account_password = CharField()
    transaction_type = IntegerField()
    start_date = DateField()
    end_date = DateField()

    def validate(self, data):
        if not data["account_number"]:
            raise BadRequestException({'message': 'ENTER_YOUR_ACCOUNT_NUMBER'})
        if data["start_date"] > data["end_date"]:
            raise BadRequestException({'message': '알맞은 날짜를 입력하세요.'})

        if not data["account_password"]:
            raise BadRequestException({'message': 'INVALID_YOUR_ACCOUNT_NUMBER'})
        return data


class TransactionListResponseSerializer(Serializer):
    transaction = TransactionModelSerializer(many=True)