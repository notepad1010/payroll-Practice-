from django.db import  models
from .employee import Employee

class BenefitType(models.Model):
     benefit_name = models.CharField(max_length=50, unique=True)
     description = models.CharField(max_length=100,blank=True)
     create_at = models.DateTimeField(auto_now_add=True)
     update_at = models.DateTimeField(auto_now=True)

     def __str__(self):
          return self.benefit_name
     class Meta:
          db_table = 'benefit_type'
     
class EmployeeBenefit(models.Model):
     employee = models.ForeignKey(Employee,
                                  on_delete=models.CASCADE,
                                  related_name='benefits')
     
     benefit = models.ForeignKey(BenefitType,
                                 on_delete=models.CASCADE,
                                 related_name='employee_benefits')
     
     amount = models.DecimalField(max_digits=10,decimal_places=2)
     effective_start_date = models.DateField()
     effective_end_date = models.DateField(null=True,blank=True)
     create_at = models.DateTimeField(auto_now_add=True)
     update_at = models.DateTimeField(auto_now=True)

     def __str__(self):
        return f"{self.employee.full_name} - {self.benefit.benefit_name}"
     class Meta:
        db_table = 'employee_benefit'
     