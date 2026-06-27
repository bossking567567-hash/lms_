from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    HomeworkViewSet,
    SubmissionViewSet,
    ProgressViewSet,
    EnrollmentViewSet,
    CourseProgressView,
    StudentDashboardView,
    TeacherDashboardView,
    generate_certificate,
)

router = DefaultRouter()

router.register(r'homeworks', HomeworkViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'progress', ProgressViewSet)
router.register(r'enrollments', EnrollmentViewSet)

urlpatterns = router.urls + [
    path('progress/<int:course_id>/', CourseProgressView.as_view()),
    path('certificate/<int:course_id>/', generate_certificate),
    path('dashboard/student/', StudentDashboardView.as_view()),
    path('dashboard/teacher/', TeacherDashboardView.as_view()),
]