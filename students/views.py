from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Avg, Count, Q
from django.http import HttpResponse
import csv
from datetime import datetime

from .models import Teacher, Classroom, Student, Subject, Score
from .serializers import (
    TeacherSerializer, ClassroomSerializer, StudentListSerializer, 
    StudentDetailSerializer, SubjectSerializer, ScoreSerializer,
    ClassroomStatsSerializer, StudentScoreHistorySerializer, ScoreCreateSerializer
)


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['full_name', 'email']
    ordering_fields = ['full_name', 'created_at']
    ordering = ['full_name']

    def get_queryset(self):
        queryset = super().get_queryset()
        # If user is a teacher, only show their own profile
        if hasattr(self.request.user, 'teacher_profile'):
            queryset = queryset.filter(user=self.request.user)
        return queryset

    @action(detail=True, methods=['get'])
    def classrooms(self, request, pk=None):
        """Get all classrooms for a specific teacher"""
        teacher = self.get_object()
        classrooms = teacher.classrooms.filter(is_active=True)
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """Get all students for a specific teacher"""
        teacher = self.get_object()
        students = Student.objects.filter(classroom__teacher=teacher, is_active=True)
        serializer = StudentListSerializer(students, many=True)
        return Response(serializer.data)


class ClassroomViewSet(viewsets.ModelViewSet):
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

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """Get all students in a classroom"""
        classroom = self.get_object()
        students = classroom.students.filter(is_active=True)
        serializer = StudentListSerializer(students, many=True)
        return Response(serializer.data)

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


class StudentViewSet(viewsets.ModelViewSet):
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


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def scores(self, request, pk=None):
        """Get all scores for a specific subject"""
        subject = self.get_object()
        scores = subject.scores.all()
        
        # Filter by classroom if user is a teacher
        if hasattr(self.request.user, 'teacher_profile'):
            scores = scores.filter(student__classroom__teacher=self.request.user.teacher_profile)
            
        serializer = ScoreSerializer(scores, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get statistics for a specific subject"""
        subject = self.get_object()
        scores = subject.scores.all()
        
        # Filter by classroom if user is a teacher
        if hasattr(self.request.user, 'teacher_profile'):
            scores = scores.filter(student__classroom__teacher=self.request.user.teacher_profile)
        
        if scores.exists():
            stats = scores.aggregate(
                average=Avg('score'),
                count=Count('id')
            )
            stats['average'] = round(stats['average'], 2) if stats['average'] else 0
        else:
            stats = {'average': 0, 'count': 0}
            
        return Response(stats)


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['student', 'subject', 'score_type', 'teacher']
    search_fields = ['student__full_name', 'subject__name']
    ordering_fields = ['date', 'score', 'created_at']
    ordering = ['-date']

    def get_queryset(self):
        queryset = super().get_queryset()
        # If user is a teacher, only show scores they gave or for their students
        if hasattr(self.request.user, 'teacher_profile'):
            queryset = queryset.filter(
                Q(teacher=self.request.user.teacher_profile) |
                Q(student__classroom__teacher=self.request.user.teacher_profile)
            )
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ScoreCreateSerializer
        return ScoreSerializer

    def perform_create(self, serializer):
        # Automatically set the teacher to the current user's teacher profile
        if hasattr(self.request.user, 'teacher_profile'):
            serializer.save(teacher=self.request.user.teacher_profile)
        else:
            serializer.save()

    @action(detail=False, methods=['get'])
    def by_classroom(self, request):
        """Get scores filtered by classroom"""
        classroom_id = request.query_params.get('classroom_id')
        if not classroom_id:
            return Response({'error': 'classroom_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        scores = self.get_queryset().filter(student__classroom_id=classroom_id)
        serializer = self.get_serializer(scores, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Create multiple scores at once"""
        data = request.data
        if not isinstance(data, list):
            return Response({'error': 'Expected a list of scores'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ScoreCreateSerializer(data=data, many=True)
        if serializer.is_valid():
            # Set teacher for all scores if user is a teacher
            if hasattr(request.user, 'teacher_profile'):
                for score_data in serializer.validated_data:
                    score_data['teacher'] = request.user.teacher_profile
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)