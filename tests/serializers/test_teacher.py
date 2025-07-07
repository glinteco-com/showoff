import pytest
from django.contrib.auth import get_user_model

from learning.models.teacher import Teacher
from learning.serializers.teacher import TeacherSerializer


@pytest.mark.django_db
def test_teacher_serializer():
    user = get_user_model().objects.create(username="teacher2")
    teacher = Teacher.objects.create(user=user)
    serializer = TeacherSerializer(teacher)
    assert serializer.data["user"]["id"] == user.id
