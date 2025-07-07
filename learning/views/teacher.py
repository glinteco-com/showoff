from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from ..models import Student, Teacher
from ..serializers import (
    ClassroomSerializer,
    StudentListSerializer,
    TeacherSerializer,
)


class TeacherViewSet(viewsets.ModelViewSet):
    """
    Teacher Management ViewSet
    """

    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["full_name", "email"]
    ordering_fields = ["full_name", "created_at"]
    ordering = ["full_name"]

    def get_queryset(self):
        queryset = super().get_queryset()
        # If user is a teacher, only show their own profile
        if hasattr(self.request.user, "teacher_profile"):
            queryset = queryset.filter(user=self.request.user)
        return queryset

    @swagger_auto_schema(
        operation_summary="Get teacher's classrooms",
        operation_description="Get all classrooms for a specific teacher",
        tags=["Teacher: Classroom Management"],
    )
    @action(detail=True, methods=["get"])
    def classrooms(self, request, pk=None):
        """Get all classrooms for a specific teacher"""
        teacher = self.get_object()
        classrooms = teacher.classrooms.filter(is_active=True)
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Get teacher's students",
        operation_description="Get all students for a specific teacher",
        tags=["Teacher: Student Management"],
    )
    @action(detail=True, methods=["get"])
    def students(self, request, pk=None):
        """Get all students for a specific teacher"""
        teacher = self.get_object()
        students = Student.objects.filter(
            classroom__teacher=teacher, is_active=True
        )
        serializer = StudentListSerializer(students, many=True)
        return Response(serializer.data)
