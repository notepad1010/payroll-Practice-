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

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only = True)
    new_password = serializers.CharField(write_only = True, min_length = 8)
    confirm_password = serializers.CharField(write_only = True)

    def validate_old_password(self,value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value
    
    def validate(self,data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'password Do not match'
            })
        return data
    
class ChangePasswordRequestSerializer(serializers.Serializer):
    company_email =serializers.EmailField()

    def validate_company_email(self,value):
        try:
            UserAccount.objects.get(company_email = value)
        except UserAccount.DoesNotExist:
            raise serializers.ValidationError('No account found with this email.')
        return value
    

class PasswordResetComfimationSerializer(serializers.Serializer):
    reset_request_id = serializers.IntegerField()
    otp = serializers.CharField(required=False, allow_blank=True)
    otp_code = serializers.CharField(required=False, allow_blank=True)
    new_password = serializers.CharField(required=False, allow_blank=True, write_only=True, min_length=8)
    
    def validate(self, data):
        # At least one OTP field should be provided
        if not data.get('otp') and not data.get('otp_code'):
            raise serializers.ValidationError('OTP is required.')
        return data
    