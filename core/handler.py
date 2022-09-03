from rest_framework.views import exception_handler


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
    return {"field": field, "message": response}


def custom_exception_handler(exc, context):
    error_response = exception_handler(exc, context)
    if error_response is not None:
        error = error_response.data

        if isinstance(error, list) and error:
            if isinstance(error[0], dict):
                error_response.data = get_error_message(error)

            elif isinstance(error[0], str):
                error_response.data = {
                    "message": error[0],
                }

        if isinstance(error, dict):
            error_response.data = get_error_message(error)

    return error_response
