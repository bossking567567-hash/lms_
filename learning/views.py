from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

from .models import Homework, Submission, Progress, Enrollment
from .serializers import (
    HomeworkSerializer,
    SubmissionSerializer,
    ProgressSerializer,
    EnrollmentSerializer
)

from courses.models import Course
from .services import get_course_progress, is_course_completed
from reportlab.pdfgen import canvas




class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [AllowAny]




class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(student_id=1)




class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(student_id=1)




class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(student_id=1)



class CourseProgressView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)

        return Response({
            "course": course.title,
            "progress": 0
        })




def generate_certificate(request, course_id):
    course = Course.objects.get(id=course_id)

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        'attachment; filename="certificate.pdf"'
    )

    p = canvas.Canvas(response)

    p.drawString(
        100,
        750,
        "CERTIFICATE OF COMPLETION"
    )

    p.drawString(
        100,
        700,
        f"Course: {course.title}"
    )

    p.drawString(
        100,
        650,
        "Status: COMPLETED"
    )

    p.showPage()
    p.save()

    return response




class StudentDashboardView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({

            "student": "test",

            "courses": []

        })




class TeacherDashboardView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({

            "teacher": "test",

            "courses": []

        })
