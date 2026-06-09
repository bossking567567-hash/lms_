from rest_framework import viewsets
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

from rest_framework.exceptions import PermissionDenied
from learning.models import Progress


def retrieve(self, request, *args, **kwargs):
    lesson = self.get_object()
    user = request.user


    if user.is_staff or user.role == "teacher":
        return super().retrieve(request, *args, **kwargs)


    if lesson.is_free:
        return super().retrieve(request, *args, **kwargs)


    progress = Progress.objects.filter(
        student=user,
        lesson=lesson
    ).first()

    if not progress or not progress.is_unlocked:
        raise PermissionDenied("Lesson locked")

    return super().retrieve(request, *args, **kwargs)