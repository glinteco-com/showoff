import pytest

from learning.models.subject import Subject


@pytest.mark.django_db
def test_create_subject():
    subject = Subject.objects.create(name="Math")
    assert subject.name == "Math"
