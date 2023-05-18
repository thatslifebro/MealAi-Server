from app.error.base import CustomException


class DuplicatedEmailException(CustomException):
    status = 409
    error_code = 1001
    error_name = "DUPLICATED_EMAIL"
    message = "중복된 Email이 존재합니다."


class NotFoundUserException(CustomException):
    status = 404
    error_code = 1002
    error_name = "USER_NOT_FOUND"
    message = "User를 찾을 수 없습니다."


class NotMatchPasswordException(CustomException):
    status = 400
    error_code = 1003
    error_name = "PASSWORD_NOT_MATCH"
    message = "패스워드가 일치하지 않습니다."


class DeletedEmailException(CustomException):
    status = 410
    error_code = 1004
    error_name = "DELETED_USER"
    message = "탈퇴한 Email입니다."
