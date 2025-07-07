import pytest
from django.contrib.auth import get_user_model

from learning.models.classroom import Classroom
from learning.models.teacher import Teacher


@pytest.mark.django_db
def test_create_classroom():
    user = get_user_model().objects.create(username="teacher2")
    teacher = Teacher.objects.create(user=user)
    classroom = Classroom.objects.create(name="A1", teacher=teacher)
    assert classroom.name == "A1"
    assert classroom.teacher == teacher
