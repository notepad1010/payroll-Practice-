from django.db import models
from django.contrib.auth.models import AbstractUser
from .role import Role
from hr.models import Employee


class UserAccount(AbstractUser):
        employee = models.OneToOneField(Employee, on_delete=models.CASCADE,related_name='user_account',null=True,blank=True)
        company_email = models.CharField(max_length=50,blank=True,null=True,unique=True)
        role = models.ForeignKey(Role,on_delete=models.SET_NULL,null = True,related_name='user_role')
        is_locked = models.BooleanField(default=False)
        last_login_at = models.DateField(null=True,blank=True)
        create_at = models.DateTimeField(auto_now_add=True)
        update_at= models.DateTimeField(auto_now=True)

        def __str__(self):
             return f'{self.employee.full_name} - {self.company_email}'
        
        class Meta:
               db_table = 'user_account'

class UserAccessLogs(models.Model):
     user_account = models.ForeignKey(UserAccount,on_delete=models.CASCADE,related_name='user_logs')
     employee = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='employee_logs')
     role = models.ForeignKey(Role,on_delete=models.CASCADE,related_name='role_logs')
     action = models.CharField(max_length=50)
     detail = models.CharField(max_length=255,blank=True)
     ip_address = models.CharField(max_length=45)
     device_info = models.CharField(max_length=255,blank=True)
     logged_at = models.DateTimeField(auto_now_add=True)

     def __str__(self):
           return f'{self.user_account.email} - {self.action}'
     
     class Meta:
           db_table = 'user_access_log'
