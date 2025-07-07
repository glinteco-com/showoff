from rest_framework import serializers
from .student import StudentListSerializer
from .subject import SubjectSerializer
from .teacher import TeacherSerializer
from ..models import Score


class ScoreSerializer(serializers.ModelSerializer):
    student = StudentListSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    subject = SubjectSerializer(read_only=True)
    subject_id = serializers.IntegerField(write_only=True)
    teacher = TeacherSerializer(read_only=True)
    teacher_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Score
        fields = ['id', 'student', 'student_id', 'subject', 'subject_id', 
                 'score', 'score_type', 'date', 'notes', 'teacher', 'teacher_id',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_score(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError("Score must be between 0 and 10")
        return value


class ScoreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['student', 'subject', 'score', 'score_type', 'date', 'notes', 'teacher']

    def validate_score(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError("Score must be between 0 and 10")
        return value