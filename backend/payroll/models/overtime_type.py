from django.db import models

class OvertimeType(models.Model):
    overtime_name = models.CharField(max_length=50,unique=True)
    multiplier = models.DecimalField(max_digits=5,decimal_places=2)
    description = models.CharField(max_length=100,blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.overtime_name
    
    class Meta:
        db_table = 'overtime_type'