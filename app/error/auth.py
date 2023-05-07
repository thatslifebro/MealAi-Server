from app.error.base import CustomException


class ExpiredAccessTokenException(CustomException):
    code = 401
    error_name = "EXPIRED_ACCESS_TOKEN"
    message = "만료된 Access Token 입니다."


class NotFoundAuthorizedHeaderException(CustomException):
    code = 400
    error_name = "NOT_FOUND_AUTH_HEADER"
    message = "Authorized- Header를 찾을 수 없습니다."


class InvalidTokenException(CustomException):
    code = 401
    error_name = "INVALID_TOKEN_TYPE"
    message = "Token type이 Bearer가 아니거나 올바른 Token이 아닙니다."


class NotMatchRefreshTokenException(CustomException):
    code = 401
    error_name = "NOT_MACTH_REFRESH_TOKEN"
    message = "DB의 Refersh Token과 일치하지 않습니다."
