from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet

router = DefaultRouter()

router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)

urlpatterns = router.urls