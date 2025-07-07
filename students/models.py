from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['full_name']


class Classroom(models.Model):
    name = models.CharField(max_length=50, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='classrooms')
    description = models.TextField(blank=True, null=True)
    grade_level = models.CharField(max_length=10, blank=True, null=True)  # e.g., "10", "11", "12"
    school_year = models.CharField(max_length=20, blank=True, null=True)  # e.g., "2024-2025"
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.teacher.full_name}"

    class Meta:
        ordering = ['name']


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    full_name = models.CharField(max_length=200)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='students')
    student_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    parent_name = models.CharField(max_length=200, blank=True, null=True)
    parent_phone = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.classroom.name}"

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    class Meta:
        ordering = ['full_name']


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)  # e.g., "MATH", "LIT", "ENG"
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Score(models.Model):
    SCORE_TYPES = [
        ('quiz', 'Quiz'),
        ('midterm', 'Midterm'),
        ('final', 'Final'),
        ('assignment', 'Assignment'),
        ('participation', 'Participation'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='scores')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='scores')
    score = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    score_type = models.CharField(max_length=20, choices=SCORE_TYPES, default='quiz')
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='scores_given')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.subject.name}: {self.score}"

    class Meta:
        ordering = ['-date', 'student__full_name']
        unique_together = ['student', 'subject', 'score_type', 'date']