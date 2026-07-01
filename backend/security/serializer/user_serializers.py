from security.models import UserAccount
from rest_framework import serializers

class userAccountSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    role_name = serializers.SerializerMethodField()

    class Meta:
        model = UserAccount
        fields = [
            'id',
            'username',
            'email',
            'employee',
            'employee_name',
            'role',
            'role_name',
            'is_active',
            'is_locked',
            'is_staff',
            'last_login_at',
            'create_at',
            'update_at',
        ]

    def get_employee_name(self,obj):
        if obj.employee:
            return obj.employee.full_name
        return None
    
    def get_role_name(self,obj):
        if obj.role:
            return obj.role.role_name
        return None
    
        
class UserAccountCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True,min_length = 8)
    confirm_password = serializers.CharField(write_only = True)

    class Meta:
        model = UserAccount
        fields = [
            'username',
            'email',
            'company_email',
            'employee',
            'role',
            'password',
            'confirm_password',
            'is_staff',
        ]
    
    def validate(self,data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'error':'password Dont Match'})
        return data
    
    def validate_employee(self,value):
        if value and UserAccount.objects.filter(employee=value).exists():
            raise serializers.ValidationError('This Employee already has a user account')
        return value
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = UserAccount(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    