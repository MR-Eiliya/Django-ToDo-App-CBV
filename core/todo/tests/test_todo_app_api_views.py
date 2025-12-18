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
class TestTaskAPIView:
    
    def test_create_task_with_valid_data(self, api_client, common_user):
        url = reverse("todo:api-v1:task-list")
        data = {
            "title" : "test task"
        }
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 201


    def test_create_task_with_invalid_data(self, api_client, common_user):
        url = reverse("todo:api-v1:task-list")
        data = {
            "titllee" : "test task"
        }
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 400

    
    def test_task_list_returns_all_tasks_for_authenticated_user(self, api_client, common_user):
        url = reverse("todo:api-v1:task-list")

        Task.objects.create(title="task 1", user=common_user)
        Task.objects.create(title="task 2", user=common_user)

        api_client.force_authenticate(user=common_user)

        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 2

    
    def test_task_detail_returns_task_for_authenticated_user(self, api_client, common_user):
        task = Task.objects.create(title="task detail", user=common_user)
        url = reverse("todo:api-v1:task-detail", kwargs={"pk":task.pk})
        api_client.force_authenticate(user=common_user)
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.data["id"] == task.id
        assert response.data["title"] == task.title



    def test_retrieve_task_detail_for_owner(self, api_client, common_user):
        task = Task.objects.create(
            title = "task title",
            user = common_user
        )
        url = reverse("todo:api-v1:task-detail", kwargs={"pk":task.id})
        api_client.force_authenticate(user=common_user)
        response = api_client.get(url)
        assert response.status_code == 200


    def test_retrieve_task_detail_for_none_owner(self, api_client, common_user, sub_user):
        task = Task.objects.create(
            title="private task", 
            user=common_user
        )
        url = reverse("todo:api-v1:task-detail", kwargs={"pk":task.id})
        api_client.force_authenticate(user=sub_user)
        response = api_client.get(url)
        assert response.status_code == 404


    def test_update_task_with_valid_data(self, api_client, common_user):
        task = Task.objects.create(
            title = "task title",
            user = common_user
        )
        url = reverse("todo:api-v1:task-detail", kwargs={"pk":task.id})
        data = {
            "title":"task title updated"
        }
        api_client.force_authenticate(user=common_user)
        response = api_client.put(url, data)
        assert response.status_code == 200
        task.refresh_from_db()
        assert task.title == "task title updated"



    def test_update_task_with_invalid_data(self, api_client, common_user):
        task = Task.objects.create(
            title = "task title",
            user = common_user
        )
        url = reverse("todo:api-v1:task-detail", kwargs={"pk":task.id})
        data = {
            "tittlee":"task title updated"
        }
        api_client.force_authenticate(user=common_user)
        response = api_client.put(url, data)
        assert response.status_code == 400
        task.refresh_from_db()
        assert task.title == "task title"


    def test_update_task_with_none_owner(self, api_client, common_user, sub_user):
        task = Task.objects.create(
            title = "task title",
            user = common_user
        )
        url = reverse("todo:api-v1:task-detail", kwargs={"pk":task.id})
        data = {
            "title":"task title updated"
        }
        api_client.force_authenticate(user=sub_user)
        response = api_client.put(url, data)
        assert response.status_code == 404


    def test_delete_task_for_owner(self, api_client, common_user):
        task = Task.objects.create(
            title="for delete",
            user= common_user
        )
        api_client.force_authenticate(user=common_user)
        url = reverse("todo:api-v1:task-detail", kwargs={"pk":task.id})
        response = api_client.delete(url)
        assert response.status_code == 204


    def test_delete_task_for_none_owner(self, api_client, common_user, sub_user):
        task = Task.objects.create(
            title="for delete",
            user=common_user
        )
        url = reverse("todo:api-v1:task-detail", kwargs={"pk":task.id})
        api_client.force_authenticate(user=sub_user)
        response = api_client.delete(url)
        assert response.status_code == 404
        assert Task.objects.filter(id=task.id).exists()


    # Testing views without authentication


    def test_task_list_without_authentication(self, api_client):
        url = reverse("todo:api-v1:task-list")
        response = api_client.get(url)
        assert response.status_code == 401


    def test_retrieve_task_without_authentication(self, api_client, common_user):
        task = Task.objects.create(
            title="test",
            user=common_user
        )
        url = reverse("todo:api-v1:task-detail", kwargs={"pk":task.id})
        response = api_client.get(url)
        assert response.status_code == 401


    def test_create_task_without_authentication(self, api_client):
        url = reverse("todo:api-v1:task-list")
        data = {
            "title":"new test task"
        }
        response = api_client.post(url, data)
        assert response.status_code == 401


    def test_update_task_without_authentication(self, api_client, common_user):
        task = Task.objects.create(
            title="test",
            user=common_user
        )
        url = reverse("todo:api-v1:task-detail", kwargs={"pk":task.id})
        data = {
            "title":"test updated"
        }
        response = api_client.put(url, data)
        assert response.status_code == 401


    def test_delete_task_without_authentication(self, api_client, common_user):
        task = Task.objects.create(
            title="test",
            user=common_user
        )
        url = reverse("todo:api-v1:task-detail", kwargs={"pk":task.id})
        response = api_client.delete(url)
        assert response.status_code == 401
        





        