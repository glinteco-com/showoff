from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Avg
from drf_yasg.utils import swagger_auto_schema

from ..models import Student, Subject
from ..serializers import StudentListSerializer, StudentDetailSerializer, StudentScoreHistorySerializer


class StudentViewSet(viewsets.ModelViewSet):
    """
    Student Management ViewSet
    """
    queryset = Student.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['classroom', 'gender', 'is_active', 'classroom__grade_level']
    search_fields = ['full_name', 'student_id', 'email']
    ordering_fields = ['full_name', 'birth_date', 'created_at']
    ordering = ['full_name']

    def get_serializer_class(self):
        if self.action in ['list']:
            return StudentListSerializer
        return StudentDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # If user is a teacher, only show students in their classrooms
        if hasattr(self.request.user, 'teacher_profile'):
            queryset = queryset.filter(classroom__teacher=self.request.user.teacher_profile)
        return queryset

    @swagger_auto_schema(
        operation_summary="Get student scores",
        operation_description="Get all scores for a specific student with optional filtering",
        tags=['Student: Score Management']
    )
    @action(detail=True, methods=['get'])
    def scores(self, request, pk=None):
        """Get all scores for a specific student"""
        student = self.get_object()
        scores = student.scores.all().order_by('-date')
        
        # Filter by subject if provided
        subject_id = request.query_params.get('subject_id')
        if subject_id:
            scores = scores.filter(subject_id=subject_id)
            
        # Filter by score type if provided
        score_type = request.query_params.get('score_type')
        if score_type:
            scores = scores.filter(score_type=score_type)

        serializer = StudentScoreHistorySerializer(scores, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Get student average by subject",
        operation_description="Get student's average score by subject",
        tags=['Student: Statistics']
    )
    @action(detail=True, methods=['get'])
    def average_by_subject(self, request, pk=None):
        """Get student's average score by subject"""
        student = self.get_object()
        subjects = Subject.objects.filter(is_active=True)
        
        averages = {}
        for subject in subjects:
            avg = student.scores.filter(subject=subject).aggregate(avg=Avg('score'))['avg']
            if avg:
                averages[subject.name] = round(avg, 2)
        
        return Response(averages)