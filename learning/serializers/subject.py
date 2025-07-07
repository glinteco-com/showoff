from rest_framework import serializers
from ..models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    scores_count = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'description', 'is_active', 'scores_count', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_scores_count(self, obj):
        return obj.scores.count()