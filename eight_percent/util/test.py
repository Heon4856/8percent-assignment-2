from django.db import connections
from django.test import  TransactionTestCase

class BaseTestCase(TransactionTestCase):

    databases = ["default", "replica"]

    @classmethod
    def setUpClass(cls):
        connections["replica"]._orig_cursor = connections["replica"].cursor
        connections["replica"].cursor = connections["default"].cursor
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        connections["replica"].cursor = connections["replica"]._orig_cursor
        super().tearDownClass()