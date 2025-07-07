from django.db import models


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    full_name = models.CharField(max_length=200)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE, related_name='students')
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