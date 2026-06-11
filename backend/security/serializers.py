from rest_framework import serializers
from django.contrib.auth import authenticate
from security.models import UserAccount

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        user = authenticate(
            username = data['username'],
            password = data['password']
        )

        if not user:
            raise serializers.ValidationError('Invalid Username or password')
        
        if user.is_locked:
            raise serializers.ValidationError('Account is Locked')
        
        data['user'] = user
        return data
    