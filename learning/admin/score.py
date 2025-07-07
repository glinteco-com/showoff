from django.contrib import admin
from ..models import Score


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