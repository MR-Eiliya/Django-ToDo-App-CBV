import pytest
from django.urls import reverse, resolve
from rest_framework.test import APIClient
from todo.api.v1.views import TaskModelViewSet


@pytest.fixture
def api_client():
    client = APIClient()
    return client


class TestTaskAPIUrls:

    def test_task_list_url_resolves(self):
        url = reverse("todo:api-v1:task-list")
        resolved = resolve(url)
        assert resolved.func.cls == TaskModelViewSet

    def test_task_detail_url_resolves(self):
        url = reverse("todo:api-v1:task-detail", kwargs={"pk": 1})
        resolved = resolve(url)
        assert resolved.func.cls == TaskModelViewSet

    @pytest.mark.django_db
    def test_task_list_url_smoke(self, api_client):
        url = reverse("todo:api-v1:task-list")
        response = api_client.get(url)
        assert response.status_code != 404

    def test_wrong_task_url_returns_404_status(self, api_client):
        response = api_client.get("/api/v1/takks/")
        assert response.status_code == 404
