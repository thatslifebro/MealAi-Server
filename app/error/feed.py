from app.error.base import CustomException


class NotFeedOwnerException(CustomException):
    code = 403
    error_name = "NotFeedOwner"
    message = "해당 피드의 작성자가 아닙니다."


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
