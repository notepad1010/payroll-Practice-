from django.db import models
from .user_account import UserAccount
from hr.models import Employee

class PasswordResetRequest(models.Model): 
     
     STATUS = [
          ('PENDING','Pending'),
          ('COMPLETED','Completed'),
          ('EXPIRED','Expired'),
          ('CANCELLED','Cancelled')
     ]
     
     user_account = models.ForeignKey(UserAccount,on_delete=models.CASCADE,related_name='reset_request')
     request_status = models.CharField(max_length=20,choices=STATUS, default='PENDING')
     request_at = models.DateField()
     complete_at = models.DateField(null=True,blank=True)
     resolved_by = models.ForeignKey(Employee,on_delete=models.SET_NULL,null=True,related_name='resolved_resets')
     create_at = models.DateTimeField(auto_now_add=True)
     update_at = models.DateTimeField(auto_now=True)

     def __str__(self):
          return f'reset request for {self.user_account.email}'
     
     class Meta:
          db_table = 'password_reset_request'

class TwoFactorCode(models.Model):
     
     PURPOSE = [
        ('LOGIN_2FA', 'Login 2FA'),
        ('PASSWORD_RESET', 'Password Reset'),
      ]
     user_account = models.ForeignKey(UserAccount,on_delete=models.CASCADE,related_name='user_factor_code')
     reset_request = models.ForeignKey(PasswordResetRequest,on_delete= models.CASCADE,related_name='request_code')
     otp_code_hash = models.CharField(max_length=255)
     purpose = models.CharField(max_length=200,choices=PURPOSE,default='LOGIN_2FA')
     expired_at = models.DateField()
     used_at = models.DateField()
     is_used = models.BooleanField(default=False)
     attemp_count = models.IntegerField()
     create_at = models.DateField(auto_now_add=True)

     def __str__(self):
          return f' 2FA for {self.user_account.email} - {self.purpose}'
     
     class Meta:
          db_table = 'two_factor_code'
