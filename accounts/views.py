from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .serializers import RegisterSerializer
from .models import User


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

def perform_create(self, serializer):
    serializer.save(created_by=self.request.user)


    class RegisterView(generics.CreateAPIView):
        serializer_class = RegisterSerializer

from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
import random

User = get_user_model()


# 1. SEND RESET CODE
class SendResetCodeView(APIView):
    def post(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"error": "User not found"}, status=404)

        code = str(random.randint(100000, 999999))
        user.verification_code = code
        user.save()

        send_mail(
            "Password Reset Code",
            f"Your reset code: {code}",
            "yourgmail@gmail.com",
            [email],
        )

        return Response({"message": "Code sent"})

class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")
        new_password = request.data.get("new_password")

        user = User.objects.filter(email=email, verification_code=code).first()

        if not user:
            return Response({"error": "Invalid code"}, status=400)

        user.set_password(new_password)
        user.verification_code = ""
        user.save()

        return Response({"message": "Password updated"})

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out"})
        except:
            return Response({"error": "Invalid token"}, status=400)