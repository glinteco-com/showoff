from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from ..models import Teacher


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


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)