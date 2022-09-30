from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if response is not None:
        customized_response = dict()
        customized_response['error'] = []

        for key, value in response.data.items():
            error = key
            customized_response['status_code'] = response.status_code
            customized_response['error'] = error
            customized_response['data'] = None
            if response.status_code == 401:
                if type(value[0]) is dict:
                    customized_response['message'] = [value[0]["message"]]
                else:
                    customized_response['message'] = [value]
            else:
                customized_response['message'] = value
            break

        response.data = customized_response

    return response
