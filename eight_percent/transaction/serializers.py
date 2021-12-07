from rest_framework.serializers import ModelSerializer

from .exceptions import BadRequestException
from .models import Account


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ['password', 'number', 'balance', 'user']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['number', 'balance', 'user']


    def validate(self, data):
        password   = data.get('password')

        if password is None:
            raise BadRequestException('name or number')

        return data
