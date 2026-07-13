from decimal import Decimal
from datetime import timedelta,datetime
from django.db import transaction
from django.utils import timezone

from hr.models import Employee,SalaryHistory,EmployeeBenefit
from attendance.models import Attendance
from contributions.models import PhilhealthContribution,SSSContribution,PagIBIGContribution,WithHoldingTaxBracket
from payroll.models import PayrollBenefit,PayrollDeduction,PayrollEarning,PayrollOvertime,PayrollResult,PayRun,EarningType,OvertimeType,DeductionType

def calculate_sss(basic_salary,pay_date):
    try:
        bracket = SSSContribution.objects.filter(
            min_salary__lte=basic_salary,
            max_salary__gte=basic_salary,
            effective_start_date__lte=pay_date
        ).filter(
            effective_end_date__isnull = True
        ).first() or SSSContribution.objects.filter(
            min_salary__lte = basic_salary,
            max_salary__gte = basic_salary,
            effective_start_date__lte=pay_date,
            effective_end_date__gte = pay_date,
        ).first()
        
        if not bracket:
            return Decimal('0.00')
        
        excess = basic_salary -bracket.excess_over
        sss = bracket.base_tax + (excess * bracket.tax_rate/ Decimal('100'))
        return sss.quantize(Decimal('0.01'))
    
    except Exception:
        return Decimal('0.00')
    
def calculate_phihealth(basic_salary, pay_date):
    try:
        bracket = PhilhealthContribution.objects.filter(
            effective_start_date__lte= pay_date,
        ).filter(effective_end_date__isnull= True).first() or PhilhealthContribution.objects.filter(
            effective_start_date__lte= pay_date,
            effective_end_date__gte= pay_date,
        ).first()
        
        if not bracket:
            return Decimal('0.00')
        
        capped_salary = max(bracket.salary_floor,min(basic_salary,bracket.salary_ceiling))
        total_premium = capped_salary * bracket.premium_rate/ Decimal('100')
        employee_share = total_premium * bracket.employee_share_ratio
        return employee_share.quantize(Decimal('0.01'))
    
    except Exception:
        return Decimal('0.00')
    
def calculate_pagibig(basic_salary, pay_date):
    try:
        bracket = PagIBIGContribution.objects.filter(
            max_salary__gte= basic_salary,
            min_salary__lte=basic_salary,
            effective_start_date__lte=pay_date,
            effective_end_date__isnull= True,
        ).filter(
            effective_end_date__isnull= True
        ).first() or PagIBIGContribution.objects.filter(
            max_salary__gte= basic_salary,
            min_salary__lte= basic_salary,
            effective_start_date__lte= pay_date,
            effective_end_date__gte= pay_date,
        ).first()
        
        if not bracket:
            return Decimal('0.00')
        
        employee_share = basic_salary * bracket.employee_share_rate/ Decimal('100')
        employee_share = min(employee_share,bracket.max_employee_share)
        return  employee_share.quantize(Decimal('0.01'))
    
    except Exception:
        return Decimal('0.00')
    
def calculation_withhoding_tax(basic_salary,pay_date):
    try:
        bracket = WithHoldingTaxBracket.objects.filter(
            min_salary__lte= basic_salary,
            max_salary__gte= basic_salary,
            effective_start_date__lte= pay_date,
        ).filter(
            effective_end_date__isnull= True
        ).first() or WithHoldingTaxBracket.objects.filter(
            min_salary__lte= basic_salary,
            max_salary__gte= basic_salary,
            effective_start_date__lte= pay_date,
            effective_end_date__gte= pay_date,
        ).first()
        
        if not bracket:
            return Decimal('0.00')
        
        excess = basic_salary -bracket.excess_over
        tax = bracket.base_tax + (excess * bracket.tax_rate / Decimal('100'))
        return max(tax,Decimal('0.00')).quantize(Decimal('0.01'))
    
    except Exception:
        return Decimal('0.00') 
    
def calculate_hours_worked(attendance_records):
    total_regular = Decimal('0.00')
    total_overtime = Decimal('0.00')
    STANDARD_HOURS = Decimal('8.00')
    
    for record in attendance_records:
        if record.attendance_status == 'ABSENT':
            continue
        
        if record.attendance_status == 'HALF_DAY':
            total_regular += Decimal('4.00')
            continue       
        
        if record.attendance_status in ('PRESENT','LATE','LEAVE'):
            if record.time_in and record.time_out:
                dt_in = datetime.combine(record.work_date,record.time_in)
                dt_out = datetime.combine(record.work_date,record.time_out)
                worked = (dt_out - dt_in).seconds / 3600
                regular = min(Decimal(str(worked)),STANDARD_HOURS)
                total_regular += regular
            else:
                total_regular += STANDARD_HOURS
        
        total_overtime += record.overtime_hours
    return total_regular.quantize(Decimal('0.01')),total_overtime.quantize(Decimal('0.01'))

@transaction.atomic
def compute_payroll_for_employee(employee,payrun):
    salary = SalaryHistory.objects.filter(
        employee=employee,
        start_date__lte= payrun.start_date,
    ).filter(
        end_date__isnull= True
    ).first() or SalaryHistory.objects.filter(
        employee=employee,
        start_date__lte= payrun.start_date,
        end_date__gte= payrun.start_date,
    ).first()
    
    if not salary:
        raise ValueError(f'No salary record found for {employee.full_name}')
    hourly_rate = salary.hourly_rate
    basic_salary = salary.basic_salary

    attendance_records = Attendance.objects.filter(
        employee= employee,
        work_date__gte = payrun.start_date,
        work_date__lte= payrun.end_date, 
    )
    
    regular_hours, overtime_hours  = calculate_hours_worked(attendance_records)
    regular_pay = (regular_hours * hourly_rate).quantize(Decimal('0.01'))
    overtime_pay = Decimal(0.00)
    overtime_type = OvertimeType.objects.first()
    if overtime_hours > 0 and overtime_type:
        overtime_pay = (
            overtime_hours * hourly_rate * overtime_type.multiplier).quantize(Decimal('0.01'))
    active_benefit = EmployeeBenefit.objects.filter(
        employee= employee,
        effective_start_date__lte= payrun.end_date,
    ).filter(
        effective_end_date__isnull=True
    ) or EmployeeBenefit.objects.filter(
        employee= employee,
        effective_start_date__lte = payrun.end_date,
        effective_end_date__gte = payrun.start_date
    )
    
    total_benefit = sum(b.amount for b in active_benefit) or Decimal('0.00')
    gross_pay = (regular_pay + overtime_pay + total_benefit).quantize(Decimal('0.01'))
    
    sss_amount = calculate_sss(basic_salary, payrun.pay_date)
    philhealth_amount = calculate_phihealth(basic_salary,payrun.pay_date)
    pagibig_amount = calculate_pagibig(basic_salary, payrun.pay_date)
    tax_amount = calculation_withhoding_tax(basic_salary,payrun.pay_date)
    
    total_deductions = (
        sss_amount + philhealth_amount + pagibig_amount + tax_amount
    ).quantize(Decimal('0.01'))
    
    net_pay = (gross_pay - total_deductions).quantize(Decimal('0.01'))
    
    PayrollResult.objects.filter(
        employee=employee,
        payrun = payrun,
        ).delete()
    
    payroll_result = PayrollResult.objects.create(
        employee=employee,
        payrun=payrun,
        total_hours_worked=regular_hours,
        gross_pay=gross_pay,
        total_deductions=total_deductions,
        net_pay=net_pay
    )
    
    regular_earning_type,_ = EarningType.objects.get_or_create(
        earning_name='Regular Pay',
        defaults = {'is_taxable': True,'description':'Regular hours worked'}
    )
    PayrollEarning.objects.create(
        payroll_result=payroll_result,
        earning_type=regular_earning_type,
        amount=regular_pay
    )
    
    if overtime_hours > 0 and overtime_type:
        PayrollOvertime.objects.create(
            payroll_result=payroll_result,
            overtime_type= overtime_type,
            hours_worked= overtime_hours,   
            hourly_rate= hourly_rate,
            amount= overtime_pay
        )
        
    for benefit in active_benefit:
        PayrollBenefit.objects.create(
            payroll_result=payroll_result,
            benefit_type=benefit.benefit,
            amount= benefit.amount
        )
        
    deduction_map = [
        ('SSS Contribution', sss_amount),
        ('PhilHealth Contribution', philhealth_amount),
        ('PagIBIG Contribution', pagibig_amount),
        ('Withhoding Tax',tax_amount),
    ]
    
    for deduction_name,amount in deduction_map:
        if amount > 0:
            deduction_type,_ = DeductionType.objects.get_or_create(
                deduction_name=deduction_name,
                defaults = {'is_taxable' : False , 'description': deduction_name}
            )
            PayrollDeduction.objects.create(
                payroll_result=payroll_result,
                deduction_type=deduction_type,
                amount=amount,
                is_taxable=False
            )
    return payroll_result

@transaction.atomic
def compute_payroll_for_payrun(payrun):
    employees = Employee.objects.filter(is_active=True)
    results = []
    errors = []
    
    for employee in employees:
        try:
            payroll_result = compute_payroll_for_employee(employee, payrun)
            results.append({
                'employee_id': employee.id,
                'employee_name' : employee.full_name,
                'gross_pay': str(payroll_result.gross_pay),
                'total_deductions' : str(payroll_result.total_deductions),
                'net_pay': str(payroll_result.net_pay),
            })
            
        except Exception as e:
            errors.append({
                'employee_id': employee.id,
                'employee_name': employee.full_name,
                'error': str(e)
            })
    return results,errors
                 