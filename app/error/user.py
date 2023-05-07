from app.error.base import CustomException


class DuplicatedEmailException(CustomException):
    code = 400
    error_name = "DUPLICATED_EMAIL"
    message = "중복된 Email이 존재합니다."


class NotFoundUserException(CustomException):
    code = 404
    error_name = "USER_NOT_FOUND"
    message = "DB에서 User를 찾을 수 없습니다."


class NotMatchPasswordException(CustomException):
    code = 401
    error_name = "PASSWORD_NOT_MATCH"
    message = "패스워드가 일치하지 않습니다."


class DeletedEmailException(CustomException):
    code = 400
    error_name = "DELETED_USER"
    message = "이미 탈퇴된 Email 입니다."
