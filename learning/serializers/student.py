from rest_framework import serializers
from .classroom import ClassroomSerializer
from ..models import Student, Score


class StudentListSerializer(serializers.ModelSerializer):
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)
    age = serializers.ReadOnlyField()

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'student_id', 'birth_date', 'age', 'gender', 
                 'classroom', 'classroom_name', 'email', 'phone', 'is_active']


class StudentDetailSerializer(serializers.ModelSerializer):
    classroom = ClassroomSerializer(read_only=True)
    classroom_id = serializers.IntegerField(write_only=True)
    age = serializers.ReadOnlyField()
    average_score = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'student_id', 'birth_date', 'age', 'gender',
                 'classroom', 'classroom_id', 'email', 'phone', 'address',
                 'parent_name', 'parent_phone', 'notes', 'is_active',
                 'average_score', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_average_score(self, obj):
        scores = obj.scores.all()
        if scores:
            return round(sum(float(score.score) for score in scores) / len(scores), 2)
        return None


class StudentScoreHistorySerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    teacher_name = serializers.CharField(source='teacher.full_name', read_only=True)

    class Meta:
        model = Score
        fields = ['id', 'subject_name', 'subject_code', 'score', 'score_type', 
                 'date', 'notes', 'teacher_name', 'created_at']