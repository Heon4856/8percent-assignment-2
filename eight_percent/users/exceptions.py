from rest_framework.exceptions import APIException


class BadRequestException(APIException):
    status_code = 400

    def __init__(self, field_name):
        self.default_detail = f"{field_name}"
        super(BadRequestException, self).__init__()


class NotFoundException(APIException):
    status_code = 404

    def __init__(self, field_name):
        self.default_detail = f"{field_name}"
        super(NotFoundException, self).__init__()


class WrongPasswordException(APIException):
    status_code = 400

    def __init__(self, field_name):
        self.default_detail = f"{field_name}"
        super(WrongPasswordException, self).__init__()