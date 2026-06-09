from django.db import models

class EarningType(models.Model):
    earning_name = models.CharField(max_length=50,unique=True)
    is_taxable = models.BooleanField(default=True)
    description = models.CharField(max_length=100,blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.earning_name
    
    class Meta:
        db_table = 'earning_type'

