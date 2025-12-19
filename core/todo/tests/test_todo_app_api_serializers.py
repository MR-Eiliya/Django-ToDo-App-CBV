import pytest
from todo.api.v1.serializers import TaskSerializer
from todo.models import Task
from accounts.models import CustomUserModel as User
from rest_framework.test import APIRequestFactory


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email="admin@admin.com", password="123", is_verified=True
    )
    return user


@pytest.fixture
def sub_user():
    user = User.objects.create_user(
        email="sub@sub.com", username="subuser", password="s/@1234567", is_verified=True
    )
    return user


@pytest.mark.django_db
class TestTaskSerializer:

    def test_task_serializer_with_valid_data(self, common_user):
        factory = APIRequestFactory()
        request = factory.post("/fake-url/")
        request.user = common_user
        data = {
            "title": "test task",
        }

        serializer = TaskSerializer(data=data, context={"request": request})
        assert serializer.is_valid() is True
        task = serializer.save(user=common_user)
        assert task.title == data["title"]
        assert task.user == common_user

    def test_task_serializer_with_invalid_data(self, common_user):
        factory = APIRequestFactory()
        request = factory.post("/fake-url/")
        request.user = common_user
        data = {
            "titllee": "test task",
        }

        serializer = TaskSerializer(data=data, context={"request": request})
        assert serializer.is_valid() is False
        assert "title" in serializer.errors

    def test_task_serializer_ignores_user_field_in_input_data(
        self, common_user, sub_user
    ):
        factory = APIRequestFactory()
        request = factory.post("/fake-url/")
        request.user = common_user
        data = {"title": "test task", "user": sub_user.id}
        serializer = TaskSerializer(data=data, context={"request": request})
        assert serializer.is_valid() is True
        task = serializer.save(user=common_user)
        assert task.user == common_user
        assert task.user != sub_user
