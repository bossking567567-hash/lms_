from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet

router = DefaultRouter()
router.register('courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]