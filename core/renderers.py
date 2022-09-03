from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response: Response = renderer_context["response"]
        if response.status_code < 400:
            formed_data = {
                "status": "SUCCESS",
                "status_code": response.status_code,
                "message": response.status_text,
                "result": data,
            }
        else:
            formed_data = {
                "status": "FAILED",
                "status_code": response.status_code,
                "message": response.status_text,
                "error": data,
            }
        renderer_context["response"].data = formed_data
        return super().render(
            formed_data,
            accepted_media_type=accepted_media_type,
            renderer_context=renderer_context,
        )
