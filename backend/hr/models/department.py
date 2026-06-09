from django.db import models

class Department(models.Model):
    department_code = models.CharField(max_length=20 , unique=True)
    department_name = models.CharField(max_length=80)
    is_active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.department_name
    
    class Meta:
        db_table = 'department'

