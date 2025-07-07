from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'teachers', views.TeacherViewSet)
router.register(r'classrooms', views.ClassroomViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'subjects', views.SubjectViewSet)
router.register(r'scores', views.ScoreViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
]