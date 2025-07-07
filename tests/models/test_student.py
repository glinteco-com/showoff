from datetime import date

import pytest
from django.contrib.auth import get_user_model

from learning.models.classroom import Classroom
from learning.models.student import Student
from learning.models.teacher import Teacher


@pytest.mark.django_db
def test_create_student():
    user = get_user_model().objects.create(username="teacher1")
    teacher = Teacher.objects.create(
        user=user, full_name="Teacher 1", email="t1@email.com"
    )
    classroom = Classroom.objects.create(name="A1", teacher=teacher)
    student = Student.objects.create(
        full_name="Student 1", birth_date=date(2010, 1, 1), classroom=classroom
    )
    assert student.full_name == "Student 1"
    assert student.classroom == classroom
