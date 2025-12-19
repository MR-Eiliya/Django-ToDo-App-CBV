from rest_framework import serializers
from ...models import Task


class TaskSerializer(serializers.ModelSerializer):
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name="get_abs_url")

    class Meta:
        model = Task
        fields = [
            "id",
            "user",
            "title",
            "is_completed",
            "relative_url",
            "absolute_url",
            "created_date",
            "updated_date",
        ]
        read_only_fields = ["user"]

    def get_abs_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def create(self, validate_data):
        validate_data["user"] = self.context["request"].user
        return super().create(validate_data)
