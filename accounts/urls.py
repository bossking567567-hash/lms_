from django.urls import path
from .views import RegisterView, SendResetCodeView, ResetPasswordView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('send-reset-code/', SendResetCodeView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
]