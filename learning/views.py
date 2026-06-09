from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Homework, Submission, Progress
from .serializers import HomeworkSerializer, SubmissionSerializer, ProgressSerializer
from .permissions import IsStudent, IsTeacher, IsAdmin


class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer



class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)



class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    permission_classes = [IsAuthenticated]

class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsTeacher()]
        return [IsAuthenticated()]

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def get_permissions(self):
        if self.action == "create":
            return [IsStudent()]
        if self.action in ["update", "partial_update"]:
            return [IsTeacher() | IsAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer

    def get_permissions(self):
        return [IsTeacher() | IsAdmin()]

from .models import Enrollment
from .serializers import EnrollmentSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


from rest_framework.views import APIView
from rest_framework.response import Response
from courses.models import Course
from .services import get_course_progress


class CourseProgressView(APIView):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)

        progress = get_course_progress(request.user, course)

        return Response({
            "course": course.title,
            "progress": progress
        })

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from rest_framework.views import APIView
from courses.models import Course
from .services import is_course_completed


def generate_certificate(request, course_id):
    course = Course.objects.get(id=course_id)

    if not is_course_completed(request.user, course):
        return HttpResponse("Not completed yet", status=403)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 750, "CERTIFICATE OF COMPLETION")
    p.drawString(100, 700, f"Student: {request.user.username}")
    p.drawString(100, 650, f"Course: {course.title}")
    p.drawString(100, 600, "Status: COMPLETED")
    p.showPage()
    p.save()

    return response

from rest_framework.views import APIView
from rest_framework.response import Response
from learning.models import Enrollment, Progress
from courses.models import Course
from .services import get_course_progress


class StudentDashboardView(APIView):
    def get(self, request):
        user = request.user

        enrollments = Enrollment.objects.filter(student=user)

        data = []

        for e in enrollments:
            course = e.course

            data.append({
                "course": course.title,
                "progress": get_course_progress(user, course),
            })

        return Response({
            "student": user.username,
            "courses": data
        })

class TeacherDashboardView(APIView):
    def get(self, request):
        user = request.user

        courses = Course.objects.filter(created_by=user)

        data = []

        for c in courses:
            students = Enrollment.objects.filter(course=c).count()

            data.append({
                "course": c.title,
                "students": students
            })

        return Response({
            "teacher": user.username,
            "courses": data
        })