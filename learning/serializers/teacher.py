from rest_framework import serializers
from .base import UserSerializer
from ..models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    classrooms_count = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'full_name', 'email', 'phone', 'classrooms_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_classrooms_count(self, obj):
        return obj.classrooms.count()