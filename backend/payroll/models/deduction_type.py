from django.db import models

class DeductionType(models.Model):
    deduction_name = models.CharField(max_length=50,unique=True)
    is_taxable = models.BooleanField(default=True)
    description = models.CharField(max_length=100,blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.deduction_name
    
    class Meta:
        db_table = 'deduction_type'