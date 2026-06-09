from django.db import models
from .employee import Employee


class SalaryHistory(models.Model):
     employee = models.ForeignKey(Employee,
                                  on_delete=models.CASCADE,
                                  related_name= 'salary_history')
     
     basic_salary = models.DecimalField(max_digits=12,decimal_places=2)
     gross_semi_monthly = models.DecimalField(max_digits=12,decimal_places=2)
     hourly_rate = models.DecimalField(max_digits=12,decimal_places=2)
     start_date = models.DateField()
     end_date = models.DateField(null=True, blank=True)
     create_at = models.DateTimeField(auto_now_add=True)
     update_at = models.DateTimeField(auto_now=True)

     def __str__(self):
          return f"{self.employee.full_name} - {self.basic_salary}"
     class Meta:
        db_table = 'salary_history'