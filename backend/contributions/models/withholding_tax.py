from django.db import models
from payroll.models import DeductionType

class WithHoldingTaxBracket(models.Model):
    deduction_type = models.ForeignKey(DeductionType,on_delete=models.CASCADE,related_name='bracket_tax')
    min_salary = models.DecimalField(max_digits=12,decimal_places=2)
    max_salary = models.DecimalField(max_digits=12,decimal_places=2)
    base_tax = models.DecimalField(max_digits=12,decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5,decimal_places=2)
    excess_over = models.DecimalField(max_digits=10,decimal_places=2)
    effective_start_date = models.DateField()
    effective_end_date = models.DateField(null=True,blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"TAX BRACKET: {self.max_salary} - {self.min_salary}"
    
    class Meta:
        db_table = 'withholding_tax_bracket'