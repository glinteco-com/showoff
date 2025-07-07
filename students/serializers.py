from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Teacher, Classroom, Student, Subject, Score


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']
        read_only_fields = ['id']


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    classrooms_count = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'full_name', 'email', 'phone', 'classrooms_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_classrooms_count(self, obj):
        return obj.classrooms.count()


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


class SubjectSerializer(serializers.ModelSerializer):
    scores_count = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'description', 'is_active', 'scores_count', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_scores_count(self, obj):
        return obj.scores.count()


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


class ClassroomStatsSerializer(serializers.Serializer):
    classroom = ClassroomSerializer(read_only=True)
    total_students = serializers.IntegerField()
    average_score_by_subject = serializers.DictField()
    overall_average = serializers.FloatField()


class StudentScoreHistorySerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    teacher_name = serializers.CharField(source='teacher.full_name', read_only=True)

    class Meta:
        model = Score
        fields = ['id', 'subject_name', 'subject_code', 'score', 'score_type', 
                 'date', 'notes', 'teacher_name', 'created_at']