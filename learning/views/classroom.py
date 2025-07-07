from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Avg
from django.http import HttpResponse
import csv
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema

from ..models import Classroom, Subject, Score
from ..serializers import ClassroomSerializer, StudentListSerializer, ClassroomStatsSerializer


class ClassroomViewSet(viewsets.ModelViewSet):
    """
    Classroom Management ViewSet
    """
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['teacher', 'grade_level', 'school_year', 'is_active']
    search_fields = ['name', 'teacher__full_name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        # If user is a teacher, only show their classrooms
        if hasattr(self.request.user, 'teacher_profile'):
            queryset = queryset.filter(teacher=self.request.user.teacher_profile)
        return queryset

    @swagger_auto_schema(
        operation_summary="Get classroom students",
        operation_description="Get all students in a classroom",
        tags=['Classroom: Student Management']
    )
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """Get all students in a classroom"""
        classroom = self.get_object()
        students = classroom.students.filter(is_active=True)
        serializer = StudentListSerializer(students, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Get classroom statistics",
        operation_description="Get classroom statistics including average scores by subject",
        tags=['Classroom: Statistics']
    )
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get classroom statistics"""
        classroom = self.get_object()
        students = classroom.students.filter(is_active=True)
        total_students = students.count()

        # Calculate average scores by subject
        subjects = Subject.objects.filter(is_active=True)
        average_score_by_subject = {}
        overall_scores = []

        for subject in subjects:
            scores = Score.objects.filter(
                student__classroom=classroom,
                subject=subject
            ).values_list('score', flat=True)
            
            if scores:
                avg_score = sum(float(score) for score in scores) / len(scores)
                average_score_by_subject[subject.name] = round(avg_score, 2)
                overall_scores.extend(scores)

        overall_average = None
        if overall_scores:
            overall_average = round(sum(float(score) for score in overall_scores) / len(overall_scores), 2)

        data = {
            'classroom': classroom,
            'total_students': total_students,
            'average_score_by_subject': average_score_by_subject,
            'overall_average': overall_average
        }

        serializer = ClassroomStatsSerializer(data)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Export students to CSV",
        operation_description="Export students list to CSV file",
        tags=['Classroom: Export']
    )
    @action(detail=True, methods=['get'])
    def export_students(self, request, pk=None):
        """Export students list to CSV"""
        classroom = self.get_object()
        students = classroom.students.filter(is_active=True)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="students_{classroom.name}_{datetime.now().strftime("%Y%m%d")}.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Full Name', 'Student ID', 'Birth Date', 'Gender', 'Email', 
            'Phone', 'Parent Name', 'Parent Phone', 'Average Score'
        ])

        for student in students:
            avg_score = student.scores.aggregate(avg=Avg('score'))['avg']
            avg_score = round(avg_score, 2) if avg_score else 'N/A'
            
            writer.writerow([
                student.full_name, student.student_id, student.birth_date,
                student.get_gender_display(), student.email, student.phone,
                student.parent_name, student.parent_phone, avg_score
            ])

        return response