from django.db import models


class Users(models.Model):
    name = models.CharField(max_length=10)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'