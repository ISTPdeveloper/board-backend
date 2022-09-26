import base64
import hashlib
import hmac
import json
import os
import random
import time
import requests
import bcrypt
from json import JSONDecodeError
from core.redis_connection import RedisConnection
from rest_framework import generics
from rest_framework.response import Response

SMS_AUTH_TIMEOUT = 300


class SMSCodeRequestView(generics.GenericAPIView):
    def __init__(self):
        super(SMSCodeRequestView, self).__init__()
        self.rd = RedisConnection()

    def make_signature(self, message):
        SECRET_KEY = bytes(os.getenv("SMS_SECRET_KEY"), "UTF-8")

        return base64.b64encode(
            hmac.new(SECRET_KEY, message, digestmod=hashlib.sha256).digest()
        )

    def post(self, request):
        try:
            data = json.loads(request.body)
            phone_number = data["phone_number"]

            random_code = str(random.randint(100000, 999999))
            hashed_random_code = bcrypt.hashpw(
                random_code.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            is_verified = 0

            auth = {
                "hashed_random_code": hashed_random_code,
                "is_verified": is_verified,
            }

            self.rd.conn.hmset(phone_number, auth)
            self.rd.conn.expire(phone_number, SMS_AUTH_TIMEOUT)

            timestamp = str(int(time.time() * 1000))
            message = (
                "POST "
                + os.getenv("SMS_URI")
                + "\n"
                + timestamp
                + "\n"
                + os.getenv("SMS_ACCESS_KEY")
            )
            message = bytes(message, "UTF-8")
            signature = self.make_signature(message)

            headers = {
                "Content-Type": "application/json; charset=UTF-8",
                "x-ncp-apigw-timestamp": timestamp,
                "x-ncp-iam-access-key": os.getenv("SMS_ACCESS_KEY"),
                "x-ncp-apigw-signature-v2": signature,
            }

            body = {
                "type": "sms",
                "contentType": "COMM",
                "countryCode": 82,
                "from": os.getenv("SMS_CALLER"),
                "content": f"[대욱 게시판] 인증번호 [{random_code}]를 입력해주세요",
                "messages": [{"to": phone_number}],
            }

            response = requests.post(
                os.getenv("SMS_URL"),
                data=json.dumps(body),
                headers=headers,
            )

            if response.status_code == 202:
                return Response(status=202)
            return Response({"message": "CODE_SEND_ERROR"}, status=400)

        except KeyError:
            return Response({"message": "KEY_ERROR"}, status=400)
        except JSONDecodeError:
            return Response({"message": "JSON_DECODE_ERROR"}, status=400)


class SMSCodeCheckView(generics.GenericAPIView):
    def __init__(self):
        super(SMSCodeCheckView, self).__init__()
        self.rd = RedisConnection()

    def post(self, request):
        try:
            data = json.loads(request.body)
            auth_code = data["auth_code"]
            phone_number = data["phone_number"]

            auth = self.rd.conn.hgetall(phone_number)
            if not auth:
                return Response({"message": "CODE_EXPIRED"}, status=400)

            hashed_random_code = auth["hashed_random_code"]

            if not bcrypt.checkpw(
                auth_code.encode("utf-8"), hashed_random_code.encode("utf-8")
            ):
                return Response({"message": "CODE_NOT_MATCHED"}, status=400)

            auth["is_verified"] = 1

            self.rd.conn.hmset(phone_number, auth)
            return Response(status=204)

        except KeyError:
            return Response({"message": "KEY_ERROR"}, status=400)
        except JSONDecodeError:
            return Response({"message": "JSON_DECODE_ERROR"}, status=400)
