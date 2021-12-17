from rest_framework.exceptions import APIException


class BadRequestException(APIException):
    status_code = 400

    def __init__(self, field_name):
        self.default_detail = f"{field_name}"
        super(BadRequestException, self).__init__()