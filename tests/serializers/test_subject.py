import pytest

from learning.models.subject import Subject
from learning.serializers.subject import SubjectSerializer


@pytest.mark.django_db
def test_subject_serializer():
    subject = Subject.objects.create(name="Chemistry")
    serializer = SubjectSerializer(subject)
    assert serializer.data["name"] == "Chemistry"
