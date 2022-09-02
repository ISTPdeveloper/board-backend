from rest_framework.views import exception_handler
from django.http import JsonResponse


def get_response(message, status_code, result="", status="FAILURE"):
    return {
        "status": status,
        "message": message,
        "result": result,
        "status_code": status_code,
    }


def get_error_message(error_dict):
    field = next(iter(error_dict))
    response = error_dict[field]

    if isinstance(response, dict):
        response = get_error_message(response)
    elif isinstance(response, list):
        response_message = response[0]
        if isinstance(response_message, dict):
            response = get_error_message(response_message)
        else:
            response = response[0]
    return {field: response}


def custom_exception_handler(exc, context):
    error_response = exception_handler(exc, context)
    if error_response is not None:
        error = error_response.data

        if isinstance(error, list) and error:
            if isinstance(error[0], dict):
                error_response.data = get_response(
                    message=get_error_message(error),
                    status_code=error_response.status_code,
                )

            elif isinstance(error[0], str):
                error_response.data = get_response(
                    message=error[0], status_code=error_response.status_code
                )

        if isinstance(error, dict):
            error_response.data = get_response(
                message=get_error_message(error), status_code=error_response.status_code
            )
    return error_response


class ExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if response.status_code == 500:
            response = get_response(
                message="일시적인 오류가 발생했어요",
                status_code=response.status_code,
            )
            return JsonResponse(response, status=500)

        if response.status_code == 404 and "Page not found" in str(response.content):
            response = get_response(
                message="페이지를 찾을 수 없어요. 올바른 URL을 입력해주세요",
                status_code=response.status_code,
            )
            return JsonResponse(response, status=404)

        return response
