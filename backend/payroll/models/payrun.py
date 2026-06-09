from django.db import models

class PayRun(models.Model):
    PAYROLL_TYPE = [
        ('SEMI_MONTLY', 'Semi Montly'),
        ('MONTHLY', 'Monthly'),
        ('WEEKLY', 'Weekly'),
        ('BI_WEEKLY','Bi Weekly'),
    ]

    start_date = models.DateField()
    end_date = models.DateField()
    pay_date = models.DateField()
    payroll_type = models.CharField(max_length=15,choices=PAYROLL_TYPE,default='SEMI_MONTHLY')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.start_date
    
    class Meta:
        db_table = 'payrun'