import pytest
from todo.models import Task
from accounts.models import CustomUserModel as User


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email="admin@admin.com",
        password="123",
        is_verified=True
    )
    return user


@pytest.mark.django_db
class TestTaskModel:

    def test_create_task(self, common_user):
        task = Task.objects.create(
            title="test task",
            user=common_user
        )
        assert task.id is not None
        assert task.title == "test task"
        assert task.user == common_user
        assert task.is_completed is False

    def test_task_str_method(self, common_user):
        task = Task.objects.create(
            title="my task",
            user=common_user
        )
        assert str(task) == "my task"

    def test_get_task_absolute_api_url(self, common_user):
        task = Task.objects.create(
            title="url task",
            user=common_user
        )
        url = task.get_absolute_api_url()
        assert f"/api/v1/task/{task.id}/" in url 