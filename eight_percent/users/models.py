from django.db import models


class Users(models.Model):
    """회원 스키마"""
    name = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'