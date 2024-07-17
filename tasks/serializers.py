# Third-party imports
from rest_framework import serializers

# Local imports
from .models import Task, User
from .utils import truncate_to_minute


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save(update_fields=['password'])

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        if password:
            instance.set_password(password)

        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'date_joined')
        read_only_fields = ('date_joined',)
        extra_kwargs = {
            'password': {'write_only': True},
        }


class TaskSerializer(serializers.ModelSerializer):
    
    def update(self, instance, validated_data):
        due_date = validated_data.pop('due_date', None)

        if due_date:
            due_date = truncate_to_minute(due_date)
            validated_data['due_date'] = due_date

        return super().update(instance, validated_data)

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'due_date', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')



