from django.db import models
from payroll.models import DeductionType

class PhilhealthContribution(models.Model):
     deduction_type = models.ForeignKey(DeductionType,on_delete=models.CASCADE,related_name='philhealth_rate')
     premium_rate = models.DecimalField(max_digits=12,decimal_places=2)
     salary_floor = models.DecimalField(max_digits=12,decimal_places=2)
     salary_ceiling = models.DecimalField(max_digits=12,decimal_places=2)
     employee_share_ratio = models.DecimalField(max_digits=5,decimal_places=4)
     employer_share_ratio = models.DecimalField(max_digits=5,decimal_places=4)
     # max_employee_share = models.DecimalField(max_digits=5,decimal_places=2)
     # max_employer_share = models.DecimalField(max_digits=5,decimal_places=2)
     effective_start_date = models.DateField()
     effective_end_date = models.DateField(null=True,blank=True)
     create_at = models.DateTimeField(auto_now_add=True)
     update_at = models.DateTimeField(auto_now=True)

     def __str__(self):
          return f"philhealth_rate {self.premium_rate}"
     
     class Meta:
          db_table = 'philhealth_contribution'