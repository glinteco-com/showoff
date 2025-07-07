from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema

from ..models import Score
from ..serializers import ScoreSerializer, ScoreCreateSerializer


class ScoreViewSet(viewsets.ModelViewSet):
    """
    Score Management ViewSet
    """
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

    @swagger_auto_schema(
        operation_summary="Get scores by classroom",
        operation_description="Get scores filtered by classroom",
        tags=['Score: Classroom Filter']
    )
    @action(detail=False, methods=['get'])
    def by_classroom(self, request):
        """Get scores filtered by classroom"""
        classroom_id = request.query_params.get('classroom_id')
        if not classroom_id:
            return Response({'error': 'classroom_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        scores = self.get_queryset().filter(student__classroom_id=classroom_id)
        serializer = self.get_serializer(scores, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Bulk create scores",
        operation_description="Create multiple scores at once",
        tags=['Score: Bulk Operations']
    )
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