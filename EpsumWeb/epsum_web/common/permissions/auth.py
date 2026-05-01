import json
from datetime import datetime
from jwcrypto.jwt import JWT
from jwcrypto.jwk import JWK
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpRequest
from common.utils import get_base64_decoded_str, get_base64_str, get_timezone, base64ofsha
from .exceptions import AutheticationFailed, ImposterException, TokenExpired
from users.models import CustomUser
from django.utils import timezone


class Authentication:
    @classmethod
    def get_key(cls, secret):
        return JWK(k=secret, kty='oct')
    
    def options(self, request: HttpRequest, *args, **kwargs):
        res = HttpResponse('', "application/json", status=200)
        res['Access-Control-Allow-Origin'] = '*'
        res["Access-Control-Allow-Headers"] = "*"
        res["Access-Control-Expose-Headers"] = "Authorization, user"
        res["Access-Control-Allow-Credentials"] = "true"
        res["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        return res
    
    def __parse_user(self, request:HttpRequest):
        try:
            header = request.META['HTTP_AUTHORIZATION']
            parts = header.split(' ')
            if parts[0] != "Authenticate":
                raise AutheticationFailed("Invalid authentication header")
            
            token = parts[1]
            decoded = get_base64_decoded_str(token)
            username, password_b64 = decoded.split(':')
            password = get_base64_decoded_str(password_b64)
            user = CustomUser.objects.get(email=username)
            if not user.is_active:
                raise AutheticationFailed("User is inactive")
            if user.check_password(password):
                user.last_login = timezone.now()
                user.save()
                return user
            raise AutheticationFailed("Invalid credentials")
        except CustomUser.DoesNotExist:
            raise AutheticationFailed("User does not exist")
        except Exception as e:
            raise AutheticationFailed(f"Authentication failed: ERR = {e}")

    def authenticate(self, request: HttpRequest):
        user = self.__parse_user(request)
        header = {"alg": "HS256"}
        claims = {
            "user": user.email,
            "created_on": str(datetime.now(tz=get_timezone())),
            "ttl":settings.TOKEN_TTL,
            "fingerprint": base64ofsha(str(user.userid)),
        }
        key = self.get_key(settings.TOKEN_SECRET)
        token = JWT(header=header, claims=claims)
        token.make_signed_token(key)
        return token.serialize(), user

class Authorization:
    def options(self, request: HttpRequest, *args, **kwargs):
        res = HttpResponse('', "application/json", status=200)
        res['Access-Control-Allow-Origin'] = '*'
        res["Access-Control-Allow-Headers"] = "*"
        res["Access-Control-Expose-Headers"] = "Authorization, user"
        res["Access-Control-Allow-Credentials"] = "true"
        res["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        return res

    def validate_token(self, token: str):
        key = JWK(k=settings.TOKEN_SECRET, kty='oct')
        signed_token = JWT(key=key, jwt=token)
        claims = json.loads(signed_token.claims)

        created_on = datetime.strptime(
            claims['created_on'], '%Y-%m-%d %H:%M:%S.%f%z'
        )
        now = datetime.now(tz=get_timezone())

        ttl_seconds = int(settings.TOKEN_TTL)
        if (now - created_on).total_seconds() > ttl_seconds:
            raise TokenExpired("Token expired")

        return claims["user"], claims["fingerprint"]

    def check_fingerprint(self, user: CustomUser, fingerprint: str):
        return base64ofsha(str(user.userid)) == fingerprint

    def authorize(self, request: HttpRequest):
        """Validate Bearer token and attach user"""
        try:
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if not auth_header:
                raise AutheticationFailed("Missing Authorization header")

            parts = auth_header.split(' ')
            if parts[0] != "Bearer":
                raise AutheticationFailed("Expected Bearer token")

            username, fingerprint = self.validate_token(parts[1])
            user = CustomUser.objects.get(email=username)

            if not user.is_active:
                raise AutheticationFailed("User is inactive")

            if not self.check_fingerprint(user, fingerprint):
                raise ImposterException("Imposter detected")

            self.user = user
            return user

        except CustomUser.DoesNotExist:
            raise AutheticationFailed("User not found")
        except Exception as e:
            raise AutheticationFailed(str(e))
