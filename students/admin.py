from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Teacher, Classroom, Student, Subject, Score


class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False
    verbose_name_plural = 'Teacher Profile'


class UserAdmin(BaseUserAdmin):
    inlines = (TeacherInline,)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'created_at']
    list_filter = ['created_at']
    search_fields = ['full_name', 'email', 'user__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher', 'grade_level', 'school_year', 'is_active', 'student_count']
    list_filter = ['grade_level', 'school_year', 'is_active', 'teacher']
    search_fields = ['name', 'teacher__full_name']
    readonly_fields = ['created_at', 'updated_at']

    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = 'Students'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'student_id', 'classroom', 'gender', 'age', 'is_active']
    list_filter = ['classroom', 'gender', 'is_active', 'classroom__grade_level']
    search_fields = ['full_name', 'student_id', 'email']
    readonly_fields = ['created_at', 'updated_at', 'age']
    fieldsets = (
        ('Basic Information', {
            'fields': ('full_name', 'student_id', 'birth_date', 'gender', 'classroom')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Parent Information', {
            'fields': ('parent_name', 'parent_phone')
        }),
        ('Additional Information', {
            'fields': ('notes', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at']


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'score', 'score_type', 'date', 'teacher']
    list_filter = ['subject', 'score_type', 'date', 'teacher', 'student__classroom']
    search_fields = ['student__full_name', 'subject__name', 'teacher__full_name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('student', 'subject', 'teacher', 'student__classroom')


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)