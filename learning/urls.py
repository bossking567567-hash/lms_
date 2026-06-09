from rest_framework.routers import DefaultRouter
from .views import HomeworkViewSet, SubmissionViewSet, ProgressViewSet

router = DefaultRouter()

router.register(r'homeworks', HomeworkViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'progress', ProgressViewSet)

urlpatterns = router.urls

from rest_framework.routers import DefaultRouter
from .views import EnrollmentViewSet

router = DefaultRouter()
router.register(r'enrollments', EnrollmentViewSet)

from django.urls import path
from .views import CourseProgressView, generate_certificate, StudentDashboardView

urlpatterns += [
    path('progress/<int:course_id>/', CourseProgressView.as_view()),
    path('certificate/<int:course_id>/', generate_certificate),
    path('dashboard/', StudentDashboardView.as_view()),
]

