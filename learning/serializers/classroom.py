from rest_framework import serializers
from .teacher import TeacherSerializer
from ..models import Classroom


class ClassroomSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)
    teacher_id = serializers.IntegerField(write_only=True)
    students_count = serializers.SerializerMethodField()

    class Meta:
        model = Classroom
        fields = ['id', 'name', 'teacher', 'teacher_id', 'description', 'grade_level', 
                 'school_year', 'is_active', 'students_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_students_count(self, obj):
        return obj.students.count()


class ClassroomStatsSerializer(serializers.Serializer):
    classroom = ClassroomSerializer(read_only=True)
    total_students = serializers.IntegerField()
    average_score_by_subject = serializers.DictField()
    overall_average = serializers.FloatField()