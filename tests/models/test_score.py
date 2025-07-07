from datetime import date

import pytest
from django.contrib.auth import get_user_model

from learning.models.classroom import Classroom
from learning.models.score import Score
from learning.models.student import Student
from learning.models.subject import Subject
from learning.models.teacher import Teacher


@pytest.mark.django_db
def test_create_score():
    user = get_user_model().objects.create(username="teacher2")
    teacher = Teacher.objects.create(
        user=user, full_name="Teacher 2", email="t2@email.com"
    )
    classroom = Classroom.objects.create(name="A2", teacher=teacher)
    student = Student.objects.create(
        full_name="Student 2", birth_date=date(2010, 2, 2), classroom=classroom
    )
    subject = Subject.objects.create(name="Physics", code="PHY")
    score = Score.objects.create(
        student=student,
        subject=subject,
        score=8.5,
        score_type="quiz",
        date=date.today(),
        teacher=teacher,
    )
    assert score.score == 8.5
