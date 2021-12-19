from rest_framework.exceptions import APIException


class BadRequestException(APIException):
    """잘못된 요청 예외"""
    status_code = 400

    def __init__(self, field_name):
        self.default_detail = f"{field_name}"
        super(BadRequestException, self).__init__()