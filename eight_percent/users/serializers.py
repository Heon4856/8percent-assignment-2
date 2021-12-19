import bcrypt
from rest_framework import serializers

from .exceptions import BadRequestException
from .models import Users


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    def validate(self, data: dict) -> dict:
        if len(data.get('name'))<2:
            raise BadRequestException({'message': '이름을 2자 이상으로 설정해주세요.'})

        return data


    def create(self, validated_data : dict) -> Users:
        new_salt = bcrypt.gensalt(12)
        hashed_password = bcrypt.hashpw(validated_data["password"].encode('utf-8'), new_salt)
        user = Users.objects.create(name=validated_data["name"], password=hashed_password.decode('utf-8'))
        return user

    class Meta:
        model = Users
        fields = ["name", "password"]