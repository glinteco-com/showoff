from datetime import date

import pytest
from django.contrib.auth import get_user_model

from learning.models.classroom import Classroom
from learning.models.score import Score
from learning.models.student import Student
from learning.models.subject import Subject
from learning.models.teacher import Teacher
from learning.serializers.score import ScoreSerializer


@pytest.mark.django_db
def test_score_serializer():
    user = get_user_model().objects.create(username="teacher4")
    teacher = Teacher.objects.create(
        user=user, full_name="Teacher 4", email="t4@email.com"
    )
    classroom = Classroom.objects.create(name="A4", teacher=teacher)
    student = Student.objects.create(
        full_name="Student 4", birth_date=date(2010, 4, 4), classroom=classroom
    )
    subject = Subject.objects.create(name="Biology", code="BIO")
    score = Score.objects.create(
        student=student,
        subject=subject,
        score=9.0,
        score_type="quiz",
        date=date.today(),
        teacher=teacher,
    )
    serializer = ScoreSerializer(score)
    assert float(serializer.data["score"]) == 9.0
