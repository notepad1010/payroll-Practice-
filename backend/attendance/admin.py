from django.contrib import admin 
from .models import Attendance, LeaveType, LeaveStatus, LeaveRequest, LeaveApproval, LeaveCredits

# Register your models here.
admin.site.register(Attendance)
admin.site.register(LeaveType)
admin.site.register(LeaveStatus)
admin.site.register(LeaveRequest)
admin.site.register(LeaveApproval)
admin.site.register(LeaveCredits)

