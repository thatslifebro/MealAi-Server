from app.error.base import CustomException


class NoFeedIdException(CustomException):
    code = 404
    error_name = "NoFeedId"
    message = "해당 아이디의 피드가 없습니다."


class DeleteFeedException(CustomException):
    code = 404
    error_name = "DeleteFeedError"
    message = "해당 피드를 삭제할 수 없습니다."


class UpdateFeedException(CustomException):
    code = 404
    error_name = "UpdateFeedError"
    message = "해당 피드를 수정할 수 없습니다."


class UnauthorizedFeedException(CustomException):
    code = 401
    error_name = "UnauthorizedFeedError"
    message = "해당 피드의 권한이 없습니다."
