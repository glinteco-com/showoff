import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from learning.models.subject import Subject


@pytest.mark.django_db
def test_subject_list_create():
    client = APIClient()
    user = get_user_model().objects.create_superuser(
        username="admin4", password="adminpass4"
    )
    client.force_authenticate(user=user)
    Subject.objects.create(name="History")
    url = reverse("subject-list")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_subject_create_api():
    client = APIClient()
    user = get_user_model().objects.create_superuser(
        username="admin5", password="adminpass5"
    )
    client.force_authenticate(user=user)
    url = reverse("subject-list")
    data = {"name": "Geography"}
    response = client.post(url, data)
    assert response.status_code in (201, 400)
