import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from learning.models.classroom import Classroom
from learning.models.teacher import Teacher


@pytest.mark.django_db
def test_classroom_list_create():
    client = APIClient()
    user = get_user_model().objects.create_user(
        username="teacher_api3", password="pass"
    )
    teacher = Teacher.objects.create(user=user)
    _ = Classroom.objects.create(name="C1", teacher=teacher)
    client.force_authenticate(user=user)
    url = reverse("classroom-list")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_classroom_create_api():
    client = APIClient()
    admin = get_user_model().objects.create_superuser(
        username="admin3", password="adminpass3"
    )
    client.force_authenticate(user=admin)
    user = get_user_model().objects.create(username="teacher_api4")
    teacher = Teacher.objects.create(user=user)
    url = reverse("classroom-list")
    data = {"name": "C2", "teacher": teacher.id}
    response = client.post(url, data)
    assert response.status_code in (201, 400)
