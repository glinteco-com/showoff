import pytest
from django.contrib.auth import get_user_model

from learning.models.classroom import Classroom
from learning.models.teacher import Teacher
from learning.serializers.classroom import ClassroomSerializer


@pytest.mark.django_db
def test_classroom_serializer():
    user = get_user_model().objects.create(username="teacher3")
    teacher = Teacher.objects.create(user=user)
    classroom = Classroom.objects.create(name="B2", teacher=teacher)
    serializer = ClassroomSerializer(classroom)
    assert serializer.data["name"] == "B2"
    assert (
        serializer.data["teacher"] == teacher.id
        or serializer.data["teacher"]["id"] == teacher.id
    )
