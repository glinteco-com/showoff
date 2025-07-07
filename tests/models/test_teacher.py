import pytest
from django.contrib.auth import get_user_model

from learning.models.teacher import Teacher


@pytest.mark.django_db
def test_create_teacher():
    user = get_user_model().objects.create(username="teacher1")
    teacher = Teacher.objects.create(user=user)
    assert teacher.user.username == "teacher1"
