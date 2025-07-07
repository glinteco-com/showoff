from django.db import models


class Classroom(models.Model):
    name = models.CharField(max_length=50, unique=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='classrooms')
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