from rest_framework import serializers
from ...models import Task
from accounts.models import Profile

class TaskSerializer(serializers.ModelSerializer):
    relative_url = serializers.URLField(source='get_absolute_api_url',read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name='get_abs_url')
    class Meta:
        model = Task
        fields = ["id","user","title","is_completed","relative_url","absolute_url","created_date","updated_date"]
        read_only_fields = ['user']


    def get_abs_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
    
    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)

        if not request.parser_context.get('kwargs').get('pk'):
            rep.pop('title', None)
            rep.pop('is_completed', None)
        
        return rep
    
    def create(self, validate_data):
        validate_data['user'] = Profile.objects.get(user__id = self.context.get('request').user.id)
        return super().create(validate_data)