from django.http import JsonResponse


class ExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)
        print(response)

        if response.status_code == 500:
            response = {
                "status_code": response.status_code,
                "message": "Internal Server Error",
                "error": {
                    "message": "일시적인 오류가 발생했어요",
                },
            }
            return JsonResponse(response, status=500)

        if response.status_code == 404 and "Page not found" in str(response.content):
            response = {
                "status_code": response.status_code,
                "message": "Not Found",
                "error": {
                    "message": "페이지를 찾을 수 없어요. 올바른 URL을 입력해주세요",
                },
            }
            return JsonResponse(data=response, status=404)
        return response
