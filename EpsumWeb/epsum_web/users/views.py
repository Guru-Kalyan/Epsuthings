from users.models import CustomUser
from django.views import View
from django.http import JsonResponse
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from common.views import CORSAPIView, AuthorizedAPIView, Authentication
from common.permissions.exceptions import AutheticationFailed, TokenExpired

class RegisterView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            email = body.get("email")
            password = body.get("password")
            if not email or not password:
                return JsonResponse({"status": "failed", "msg": "Email and password required"}, status=400)

            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({"status": "failed","msg": "User already exists"}, status=400)

            user = CustomUser.objects.create_user(email=email, password=password)
            return JsonResponse({"status": "success", "user": user.email}, status=201)
        except Exception as e:
            return JsonResponse({"status": "failed","msg": f"Error: {str(e)}"}, status=400)

class LoginView(Authentication, CORSAPIView):
    def post(self, request, *args, **kwargs):
        try:
            token, user = Authentication.authenticate(self, request)
            res = JsonResponse({"status": "success", "token": token, "user": user.email})
            res["Authorization"] = token
            res["user"] = user.email
            return res
        except AutheticationFailed as e:
            return JsonResponse({"status": "failed", "msg": str(e)}, status=401)

class AuthAPIView(AuthorizedAPIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"status": "success", "user": self.user.email})
