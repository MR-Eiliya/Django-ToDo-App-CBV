import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from todo.models import Task
from accounts.models import CustomUserModel as User


@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def common_user():
    user = User.objects.create_user(email="admin@admin.com",
                                               password="123",
                                               is_verified=True)
    return user

@pytest.fixture
def sub_user():
    user = User.objects.create_user(
            email="sub@sub.com",
            username="subuser",
            password="s/@1234567",
            is_verified=True
        )
    return user


@pytest.mark.django_db
class TestTaskAPIPermissions:

    def test_user_cannot_retrieve_another_users_task(self, api_client, common_user, sub_user):
        task = Task.objects.create(
            title="test task",
            user=common_user
        )
        api_client.force_authenticate(user=sub_user)
        url = reverse("todo:api-v1:task-detail", kwargs={"pk":task.id})
        response = api_client.get(url)
        assert response.status_code == 404

    
    def test_user_cannot_update_another_users_task(self, api_client, common_user, sub_user):
        task = Task.objects.create(
            title="private task",
            user=common_user
        )
        api_client.force_authenticate(user=sub_user)
        url = reverse("todo:api-v1:task-detail", kwargs={"pk":task.id})
        data = {
            "title" : "task stealing"
        }
        response = api_client.put(url, data)
        assert response.status_code == 404

    def test_user_cannot_delete_another_users_task(self, api_client, common_user, sub_user):
        task = Task.objects.create(
            title="private task",
            user=common_user
        )
        api_client.force_authenticate(user=sub_user)
        url = reverse("todo:api-v1:task-detail", kwargs={"pk":task.id})
        response = api_client.delete(url)
        assert response.status_code == 404
        assert Task.objects.filter(id=task.id).exists()