from django_filters.rest_framework import DjangoFilterBackend


def get_schema_fields(self, view):
    return []


def get_schema_operation_parameters(self, view):
    return []


DjangoFilterBackend.get_schema_fields = get_schema_fields
DjangoFilterBackend.get_schema_operation_parameters = get_schema_operation_parameters
