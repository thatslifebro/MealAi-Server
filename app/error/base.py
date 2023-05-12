from http import HTTPStatus


class CustomException(Exception):
    status = HTTPStatus.BAD_GATEWAY
    error_code = HTTPStatus.BAD_GATEWAY
    error_name = HTTPStatus.BAD_GATEWAY.phrase
    message = HTTPStatus.BAD_GATEWAY.description
