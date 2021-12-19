from rest_framework.fields import CharField, DateField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer

from .exceptions import BadRequestException
from .models import Account, Transaction


class AccountSerializer(ModelSerializer):
    user_name = CharField(source='user.name', required=False)

    class Meta:
        model = Account
        fields = ['password', 'number', 'balance', 'user_name']
        extra_kwargs = {'password': {'write_only': True} }
        read_only_fields = ['user_name', 'number', 'balance']

    def validate(self, data : dict) -> dict:
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

    def validate(self, data :dict) -> dict:
        if data.get('amount') < 1:
            raise BadRequestException({'message': '알맞은 숫자의 amount를 입력하세요.'})
        return data


class TransactionModelSerializer(ModelSerializer):

    class Meta:
        model = Transaction
        fields = [ "amount", "created_at", "description", "counterparty", "balance","transaction_type", "account"]


class TransactionListSerializer(Serializer):
    account_number = CharField()
    account_password = CharField()
    transaction_type = IntegerField()
    start_date = DateField()
    end_date = DateField()

    def validate(self, data: dict) -> dict:
        if not data.get('account_number'):
            raise BadRequestException({'message': 'ENTER_YOUR_ACCOUNT_NUMBER'})
        if data.get('start_date') > data.get('end_date'):
            raise BadRequestException({'message': '알맞은 날짜를 입력하세요.'})

        if not data.get('account_password'):
            raise BadRequestException({'message': 'INVALID_YOUR_ACCOUNT_NUMBER'})
        return data


class TransactionListResponseSerializer(Serializer):
    transaction = TransactionModelSerializer(many=True)
