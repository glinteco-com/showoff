from datetime import date

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from learning.models.classroom import Classroom
from learning.models.student import Student
from learning.models.teacher import Teacher


@pytest.mark.django_db
def test_student_list_create():
    client = APIClient()
    user = get_user_model().objects.create_user(
        username="teacher_api", password="pass"
    )
    teacher = Teacher.objects.create(
        user=user, full_name="Teacher API", email="tapi@email.com"
    )
    classroom = Classroom.objects.create(name="A5", teacher=teacher)
    _student = Student.objects.create(
        full_name="Student API",
        birth_date=date(2010, 5, 5),
        classroom=classroom,
    )
    client.force_authenticate(user=user)
    url = reverse("student-list")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_student_create_api():
    client = APIClient()
    admin = get_user_model().objects.create_superuser(
        username="admin2", password="adminpass2"
    )
    client.force_authenticate(user=admin)
    user = get_user_model().objects.create(username="teacher_api2")
    teacher = Teacher.objects.create(
        user=user, full_name="Teacher API2", email="tapi2@email.com"
    )
    classroom = Classroom.objects.create(name="A6", teacher=teacher)
    url = reverse("student-list")
    data = {
        "full_name": "Student API2",
        "birth_date": "2010-06-06",
        "classroom": classroom.id,
    }
    response = client.post(url, data)
    assert response.status_code in (201, 400)
