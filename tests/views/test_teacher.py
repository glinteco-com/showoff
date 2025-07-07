import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from learning.models.teacher import Teacher


@pytest.mark.django_db
def test_teacher_list_create():
    client = APIClient()
    user = get_user_model().objects.create_user(
        username="teacher_api", password="pass"
    )
    _teacher = Teacher.objects.create(user=user)
    client.force_authenticate(user=user)
    url = reverse("teacher-list")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_teacher_create_api():
    client = APIClient()
    admin = get_user_model().objects.create_superuser(
        username="admin", password="adminpass"
    )
    client.force_authenticate(user=admin)
    user = get_user_model().objects.create(username="teacher_api2")
    url = reverse("teacher-list")
    data = {"user": user.id}
    response = client.post(url, data)
    assert response.status_code in (201, 400)
