from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Score(models.Model):
    SCORE_TYPES = [
        ('quiz', 'Quiz'),
        ('midterm', 'Midterm'),
        ('final', 'Final'),
        ('assignment', 'Assignment'),
        ('participation', 'Participation'),
    ]

    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='scores')
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='scores')
    score = models.DecimalField(
        max_digits=4, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    score_type = models.CharField(max_length=20, choices=SCORE_TYPES, default='quiz')
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='scores_given')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.subject.name}: {self.score}"

    class Meta:
        ordering = ['-date', 'student__full_name']
        unique_together = ['student', 'subject', 'score_type', 'date']