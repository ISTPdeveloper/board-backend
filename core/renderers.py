from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse


class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response: JsonResponse = renderer_context["response"].data

        return super().render(
            response,
            accepted_media_type=accepted_media_type,
            renderer_context=renderer_context,
        )
