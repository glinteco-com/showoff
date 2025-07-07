from django.contrib import admin
from ..models import Classroom


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher', 'grade_level', 'school_year', 'is_active', 'student_count']
    list_filter = ['grade_level', 'school_year', 'is_active', 'teacher']
    search_fields = ['name', 'teacher__full_name']
    readonly_fields = ['created_at', 'updated_at']

    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = 'Students'