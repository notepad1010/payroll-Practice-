from decimal import Decimal
from django.db import transaction
from attendance.models import LeaveApproval,LeaveCredits,LeaveRequest,LeaveStatus,LeaveType

@transaction.atomic
def process_leave_approval(leave_approval):
    leave_request = leave_approval.leave_request
    employee = leave_request.employee
    leave_type = leave_request.leave_type
    leave_hours = leave_request.leave_hours
    year = leave_request.start_date.year
    leave_days = Decimal(str(leave_hours)) / Decimal('8.00')
    
    try:
        leave_credits = LeaveCredits.objects.get(
            employee=employee,
            leave_type=leave_type,
            year=year
        )
    except LeaveCredits.DoesNotExist:
        raise ValueError(
            f'No leave credits found for {employee.full_name}'
           f'- {leave_type} for year {year}'
        )
        
    if leave_credits.remaining_credits < leave_days:
        raise ValueError(
            f'Insufficient leave credits . '
            f'Requested: {leave_days}'
            f'Remaining: {leave_credits.remaining_credits}'
        )
    
    leave_credits.used_credits += leave_days
    leave_credits.remaining_credits -= leave_days
    leave_credits.save()
    
    try:
        approved_status = LeaveStatus.objects.get(leave_status_name='APPROVED')
        leave_request.leave_status = approved_status
        leave_request.save()
    except LeaveStatus.DoesNotExist:
        raise ValueError(' APPROVED status not found. please seed LeaveStatus table.')
    
    return leave_credits


@transaction.atomic
def reverse_leave_approval(leave_approval):
    
    leave_request = leave_approval.leave_request
    employee = leave_request.employee
    leave_type = leave_request.leave_type
    leave_hours = leave_request.leave_hours
    year = leave_request.start_date.year    
    leave_day = Decimal(str(leave_hours)) / Decimal('8.00')
    
    try:
        leave_credits = LeaveCredits.objects.get(
            employee=employee,
            leave_type=leave_type,
            year=year
        )
    except LeaveCredits.DoesNotExist:
        raise ValueError(
            f'No leave credits found for {employee.full_name}'
            f'- {leave_type.leave_name} for year {year}'
        )
        
    leave_credits.used_credits -= leave_day
    leave_credits.remaining_credits  += leave_day
    leave_credits.save()
    
    try:
        pending_status = LeaveStatus.objects.get(leave_status_name='PENDING')
        leave_request.leave_status = pending_status
        leave_request.save()
    except LeaveStatus.DoesNotExist:
        raise ValueError('PENDING status not found. please seed LeaveStatus table')
    
    return leave_credits


    

    