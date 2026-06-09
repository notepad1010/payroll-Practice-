from django.db import models
from payroll.models import DeductionType

class  PagIBIGContribution(models.Model):
     deduction_type = models.ForeignKey(DeductionType,on_delete=models.CASCADE,related_name='pagibig_rate')
     min_salary = models.DecimalField(max_digits=12,decimal_places=2)
     max_salary = models.DecimalField(max_digits=12,decimal_places=2)
     employee_share_rate = models.DecimalField(max_digits=12,decimal_places=2)
     employer_share_rate = models.DecimalField(max_digits=12,decimal_places=2)
     max_employee_share = models.DecimalField(max_digits=12,decimal_places=2)
     max_employer_share = models.DecimalField(max_digits=12,decimal_places=2)
     effective_start_date = models.DateField()
     effective_end_date = models.DateField(null=True,blank=True)
     create_at = models.DateTimeField(auto_now_add=True)
     update_at = models.DateTimeField(auto_now=True)

     def __str__(self):
          return f"{self.deduction_type.deduction_name} PagIBIG Rate {self.min_salary} - {self.max_salary}"
     
     class Meta:
          db_table = 'pagibig_contribution' 
