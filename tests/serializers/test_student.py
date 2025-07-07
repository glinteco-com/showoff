from datetime import date

import pytest
from django.contrib.auth import get_user_model

from learning.models.classroom import Classroom
from learning.models.student import Student
from learning.models.teacher import Teacher
from learning.serializers.student import StudentListSerializer


@pytest.mark.django_db
def test_student_list_serializer():
    user = get_user_model().objects.create(username="teacher3")
    teacher = Teacher.objects.create(
        user=user, full_name="Teacher 3", email="t3@email.com"
    )
    classroom = Classroom.objects.create(name="A3", teacher=teacher)
    student = Student.objects.create(
        full_name="Student 3", birth_date=date(2010, 3, 3), classroom=classroom
    )
    serializer = StudentListSerializer(student)
    assert serializer.data["full_name"] == "Student 3"
