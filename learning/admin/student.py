from django.contrib import admin
from ..models import Student


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