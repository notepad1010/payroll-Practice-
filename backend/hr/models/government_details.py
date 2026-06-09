from django.db import models
from .employee import Employee

class GovernmentDetails(models.Model):
        employee = models.OneToOneField(Employee,
                                        on_delete=models.CASCADE,
                                        related_name='government_details')
        
        sss_number = models.CharField(max_length=45,unique=True)
        tin_number = models.CharField(max_length=45,unique=True)
        pagibig_number = models.CharField(max_length=45,unique=True)
        philhealth_number = models.CharField(max_length=45, unique=True)
        create_at = models.DateTimeField(auto_now_add=True)
        update_at = models.DateTimeField(auto_now=True)

        def __str__(self):
             return f"{self.employee.full_name} - Government Details"
        class Meta:
             db_table = 'government_details'