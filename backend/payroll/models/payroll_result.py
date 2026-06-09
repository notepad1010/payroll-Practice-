from django.db import models
from hr.models import Employee,BenefitType
from .payrun import PayRun
from .earning_type import EarningType
from .deduction_type import DeductionType
from .overtime_type import OvertimeType


class PayrollResult(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='payroll_results')
    payrun = models.ForeignKey(PayRun,on_delete=models.CASCADE,related_name='results')
    total_hours_worked = models.DecimalField(max_digits=12,decimal_places=2)
    gross_pay = models.DecimalField(max_digits=12,decimal_places=2)
    total_deductions = models.DecimalField(max_digits=12,decimal_places=2)
    net_pay = models.DecimalField(max_digits=12,decimal_places=2)
    generate_at =models.DateTimeField(auto_now_add=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.employee.full_name} - {self.payrun}'
    
    class Meta:
        db_table = 'payroll_result'

class PayrollEarning(models.Model):
    payroll_result = models.ForeignKey(PayrollResult,on_delete=models.CASCADE,related_name='earnings')
    earning_type = models.ForeignKey(EarningType,on_delete=models.CASCADE,related_name='payroll_earnings')
    amount = models.DecimalField(max_digits=12,decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.payroll_result.employee.full_name} - {self.earning_type.earning_name}'
    
    class Meta:
        db_table = 'payroll_earning'

class PayrollDeduction(models.Model):
    payroll_result = models.ForeignKey(PayrollResult,on_delete=models.CASCADE,related_name='deductions')
    deduction_type = models.ForeignKey(DeductionType,on_delete=models.CASCADE,related_name='payroll_deductions')
    amount = models.DecimalField(max_digits=12,decimal_places=2)
    is_taxable = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.payroll_result} - {self.deduction_type.deduction_name}'
    
    class Meta:
        db_table = 'payroll_deduction'

class PayrollBenefit(models.Model):
    payroll_result = models.ForeignKey(PayrollResult,on_delete=models.CASCADE,related_name='benefits') 
    benefit_type = models.ForeignKey(BenefitType,on_delete=models.CASCADE,related_name='benefits_types')
    amount = models.DecimalField(max_digits=12,decimal_places=2)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.payroll_result} - {self.benefit_type.benefit_name}'
    
    class Meta:
        db_table = 'payroll_benefit'

class PayrollOvertime(models.Model):
    payroll_result = models.ForeignKey(PayrollResult,on_delete=models.CASCADE,related_name='overtimes')
    overtime_type = models.ForeignKey(OvertimeType,on_delete=models.CASCADE,related_name='payroll_overtimes')
    hours_worked = models.DecimalField(max_digits=10,decimal_places=2)
    hourly_rate = models.DecimalField(max_digits=12,decimal_places=2)
    amount = models.DecimalField(max_digits=12,decimal_places=2)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.payroll_result} - {self.overtime_type.overtime_name}'
    
    class Meta:
        db_table = 'payroll_overtime'