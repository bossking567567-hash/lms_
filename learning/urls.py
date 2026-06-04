from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LessonViewSet, HomeworkViewSet, SubmissionViewSet

router = DefaultRouter()
router.register('lessons', LessonViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

router.register('homeworks', HomeworkViewSet)

router.register('submissions', SubmissionViewSet)