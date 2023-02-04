from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model


class UserSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=20)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

    def validate_username(self, value):
        '''
            Custom validation when user try to signup with already in user username
        '''
        query_user = User.objects.filter(username=value)

        if (len(query_user) > 0):
            raise serializers.ValidationError(
                {'error': 'The username is already in use'})
        return value

    def create(self, validated_data):
        current_password = validated_data['password']
        user = User(**validated_data)
        user.set_password(current_password)
        user.save()
        return user
