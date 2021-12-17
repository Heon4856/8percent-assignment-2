from rest_framework import serializers

import bcrypt

from .models import Users


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    def create(self, validated_data):
        new_salt = bcrypt.gensalt(12)
        hashed_password = bcrypt.hashpw(validated_data["password"].encode('utf-8'), new_salt)
        user = Users.objects.create(name=validated_data["name"], password=hashed_password.decode('utf-8'))
        return user

    class Meta:
        model = Users
        fields = ["name", "password"]