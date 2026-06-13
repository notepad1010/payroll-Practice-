from security.models import Role,RolePermission,Permission
from rest_framework import serializers

class PermissionSerializer(serializers.ModelField):
    class Meta:
        model = Permission
        fields = '__all__'
        read_only_fields = ['create_at','update_at']

class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    Permission = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = [
            'id',
            'role_name',
            'description',
            'permission',
            'create_at',
            'update_at'
        ]

        read_only_fields = ['create_at','update_at']

        def get_permission(self,obj):
            role_permission = RolePermission.objects.filter(role = obj).select_related('permission')

            return[{
                'id':rp.permission.id,
                'permission_key':rp.permission.permission_key,
                'description': rp.permission.description,
            }
            for rp in Permission
            ]