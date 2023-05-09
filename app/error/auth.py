from app.error.base import CustomException


class ExpiredAccessTokenException(CustomException):
    status = 401
    error_code = 2001
    error_name = "EXPIRED_ACCESS_TOKEN"
    message = "만료된 Access Token 입니다."


class ExpiredRefreshTokenException(CustomException):
    status = 401
    error_code = 2002
    error_name = "EXPIRED_REFRESH_TOKEN"
    message = "만료된 Refresh Token 입니다."


class NotFoundAuthorizedHeaderException(CustomException):
    status = 400
    error_code = 2003
    error_name = "NOT_FOUND_AUTH_HEADER"
    message = "Authorization- Header를 찾을 수 없습니다."


class InvalidTokenException(CustomException):
    status = 401
    error_code = 2004
    error_name = "INVALID_TOKEN_TYPE"
    message = "Token type이 Bearer가 아니거나 올바른 Token이 아닙니다."


class NotMatchRefreshTokenException(CustomException):
    status = 401
    error_code = 2005
    error_name = "NOT_MACTH_REFRESH_TOKEN"
    message = "DB의 Refersh Token과 일치하지 않습니다."


class TokenIsBlacklist(CustomException):
    status = 401
    error_code = 2006
    error_name = "TOKEN_IS_BLACKLIST"
    message = "Blacklist에 있는 Access Token 입니다."
