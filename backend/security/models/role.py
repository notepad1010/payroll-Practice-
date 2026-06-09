from django.db import models

class Role(models.Model):
    role_name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=250,null=True,blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return f'{self.role_name}'

    class Meta:
         db_table = 'role'

class Permission(models.Model):
    permission_key = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=250,null=True,blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return f'Permission: {self.permission_key}'
    
    class Meta:
         db_table = 'permission'



class RolePermission(models.Model):
    role = models.ForeignKey(Role,on_delete=models.CASCADE,related_name='permissions')
    permission = models.ForeignKey(Permission,on_delete=models.CASCADE,related_name='roles') 
    create_at = models.DateField(auto_now_add=True)

    def __str__(self):
         return f'Permission Role : {self.role.role_name} - {self.permission.permission_key}'
    
    class Meta:
         db_table = 'role_permission'