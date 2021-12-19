from rest_framework.exceptions import APIException


class BadRequestException(APIException):
    """잘못된 요청일 때 예외처리"""
    status_code = 400

    def __init__(self, field_name):
        self.default_detail = f"{field_name}"
        super(BadRequestException, self).__init__()


class NotFoundException(APIException):
    """db에서 찾을 수 없을 때 예외처리"""
    status_code = 404

    def __init__(self, field_name):
        self.default_detail = f"{field_name}"
        super(NotFoundException, self).__init__()


class WrongPasswordException(APIException):
    """db에 저장된 비밀번호와 일치하지 않을 때"""
    status_code = 400

    def __init__(self, field_name):
        self.default_detail = f"{field_name}"
        super(WrongPasswordException, self).__init__()