from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Lesson, Submission
from .serializers import LessonSerializer, SubmissionSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

from rest_framework import viewsets
from .models import Homework
from .serializers import HomeworkSerializer


class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

from rest_framework.response import Response


def retrieve(self, request, *args, **kwargs):
    lesson = self.get_object()

    allowed = True  # keyin login qo‘shamiz

    if not allowed:
        return Response({"error": "Locked"}, status=403)

    return super().retrieve(request, *args, **kwargs)

from rest_framework import viewsets
from .models import Submission
from .serializers import SubmissionSerializer
from .permissions import IsAdminUser


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [IsAdminUser()]
        return super().get_permissions()

from rest_framework.response import Response
from rest_framework import status
from .services import is_lesson_unlocked


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def retrieve(self, request, *args, **kwargs):
        lesson = self.get_object()

        if not is_lesson_unlocked(request.user, lesson):
            return Response(
                {"error": "Lesson locked. Homework not approved."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().retrieve(request, *args, **kwargs)