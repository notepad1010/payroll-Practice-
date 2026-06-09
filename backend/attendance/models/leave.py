from django.db import models  
from hr.models import Employee  


class LeaveType(models.Model):
    leave_name = models.CharField(max_length=50, unique=True)
    default_credits = models.DecimalField(max_digits=12,decimal_places=2)
    is_paid = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.leave_name}'
    
    class Meta:
        db_table = 'leave_type'

class LeaveStatus(models.Model):

    LEAVE_STATUS = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    ]

    leave_status_name = models.CharField(max_length=10,
                                         choices=LEAVE_STATUS,
                                         unique=True)
    
    description = models.CharField(max_length=250,blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.leave_status_name
    
    class Meta:
        db_table = 'leave_status'

class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name="leave_requests")
    leave_type = models.ForeignKey(LeaveType,on_delete=models.CASCADE,related_name='requests')
    leave_status = models.ForeignKey(LeaveStatus,on_delete=models.CASCADE,related_name='leave_statuses')
    start_date = models.DateField()
    end_date = models.DateField(null=True,blank=True)
    leave_hours = models.DecimalField(max_digits=5,decimal_places=2)
    reason = models.CharField(max_length=255)
    date_submitted = models.DateTimeField(auto_now_add=True)
    create_at =  models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.employee.full_name} - {self.leave_type.leave_name}'
    
    class Meta:
        db_table = 'leave_request'

class LeaveApproval(models.Model):
    leave_request = models.ForeignKey(LeaveRequest,on_delete=models.CASCADE,related_name='approvals')
    approved_by = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='approvals_given')
    remarks = models.CharField(max_length=255,blank=True)
    approved_at = models.DateTimeField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Approval for {self.leave_request}'
    
    class Meta:
        db_table = 'leave_approval'

class LeaveCredits(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='leave_credits')
    leave_type = models.ForeignKey(LeaveType,on_delete=models.CASCADE,related_name='credits')
    total_credits = models.DecimalField(max_digits=5,decimal_places=2)
    used_credits = models.DecimalField(max_digits=5,decimal_places=2,default=0)
    remaining_credits = models.DecimalField(max_digits=5,decimal_places=2)
    year = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee.full_name} - {self.leave_type.leave_name} - {self.year}"
    
    class Meta:
        db_table = 'leave_credits'