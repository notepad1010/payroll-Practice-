from django.db import models
from hr.models import Employee 

class Attendance(models.Model):
    ATTENDANCE_STATUS = [
        ('PRESENT','Present'),
        ('LATE','Late'),
        ('ABSENT','Absent'),
        ('HALF_DAY', 'Half Day'),
        ('LEAVE', 'On Leave')
    ]

    employee = models.ForeignKey(Employee,
                                on_delete=models.CASCADE,
                                related_name='attendances')
    
    work_date = models.DateField()
    time_in = models.TimeField(null=True, blank= True)
    time_out = models.TimeField(null=True, blank=True)
    overtime_hours = models.DecimalField(max_digits=5,
                                         decimal_places=2,
                                         default=0)
    
    attendance_status = models.CharField(max_length=10,
                                         choices=ATTENDANCE_STATUS,
                                         default='PRESENT')
    
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
     return f"{self.employee.full_name} - {self.work_date}"
    
    class Meta:
        unique_together = ['employee','work_date']        
        db_table = 'attendance'