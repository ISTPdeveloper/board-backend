from django.urls import path

from core.views.sms import SMSCodeCheckView, SMSCodeRequestView


app_name = "core"
urlpatterns = [
    path("sms/", SMSCodeRequestView.as_view(), name="sms 요청"),
    path("sms/verify/", SMSCodeCheckView.as_view(), name="sms 검사"),
]
