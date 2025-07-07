from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Avg, Count
from drf_yasg.utils import swagger_auto_schema

from ..models import Subject
from ..serializers import SubjectSerializer, ScoreSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    """
    Subject Management ViewSet
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']

    @swagger_auto_schema(
        operation_summary="Get subject scores",
        operation_description="Get all scores for a specific subject",
        tags=['Subject: Score Management']
    )
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

    @swagger_auto_schema(
        operation_summary="Get subject statistics",
        operation_description="Get statistics for a specific subject including average and count",
        tags=['Subject: Statistics']
    )
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