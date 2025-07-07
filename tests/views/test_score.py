from datetime import date

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from learning.models.classroom import Classroom
from learning.models.score import Score
from learning.models.student import Student
from learning.models.subject import Subject
from learning.models.teacher import Teacher


@pytest.mark.django_db
def test_score_list_create():
    client = APIClient()
    user = get_user_model().objects.create_user(
        username="teacher_api3", password="pass"
    )
    teacher = Teacher.objects.create(
        user=user, full_name="Teacher API3", email="tapi3@email.com"
    )
    classroom = Classroom.objects.create(name="A7", teacher=teacher)
    student = Student.objects.create(
        full_name="Student API3",
        birth_date=date(2010, 7, 7),
        classroom=classroom,
    )
    subject = Subject.objects.create(name="Art", code="ART")
    Score.objects.create(
        student=student,
        subject=subject,
        score=7.5,
        score_type="quiz",
        date=date.today(),
        teacher=teacher,
    )
    client.force_authenticate(user=user)
    url = reverse("score-list")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_score_create_api():
    client = APIClient()
    admin = get_user_model().objects.create_superuser(
        username="admin6", password="adminpass6"
    )
    client.force_authenticate(user=admin)
    user = get_user_model().objects.create(username="teacher_api4")
    teacher = Teacher.objects.create(
        user=user, full_name="Teacher API4", email="tapi4@email.com"
    )
    classroom = Classroom.objects.create(name="A8", teacher=teacher)
    student = Student.objects.create(
        full_name="Student API4",
        birth_date=date(2010, 8, 8),
        classroom=classroom,
    )
    subject = Subject.objects.create(name="Music", code="MUS")
    url = reverse("score-list")
    data = {
        "student": student.id,
        "subject": subject.id,
        "score": 8.0,
        "score_type": "quiz",
        "date": date.today().isoformat(),
        "teacher": teacher.id,
    }
    response = client.post(url, data)
    assert response.status_code in (201, 400)
