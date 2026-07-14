from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from payroll.models import PayRun,PayrollResult,PayrollOvertime,PayrollBenefit,PayrollDeduction,PayrollEarning
from hr.models import Employee
from decimal import Decimal



class PayslipView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request,payrun_id,employee_id):
        try:
            payrun = PayRun.objects.get(pk = payrun_id)
        except PayRun.DoesNotExist:
            return Response({'error':'Payrun not found'},status=status.HTTP_404_NOT_FOUND)
        
        try:
            employee = Employee.objects.select_related('position','department').get(pk = employee_id)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'},status=status.HTTP_404_NOT_FOUND)
        
        try:
            payroll_result = PayrollResult.objects.get( payrun=payrun,employee=employee)
        except PayrollResult.DoesNotExist:
            return Response({'error':'No payroll result found. Please compute payroll first.'},status=status.HTTP_404_NOT_FOUND)
        
        earnings = []
        total_earning = Decimal('0.00')
        for earning in PayrollEarning.objects.filter(payroll_result=payroll_result).select_related('earning_type'):
            earnings.append({
                'name':earning.earning_type.earning_name,
                'taxable': earning.earning_type.is_taxable,
                'amount': str(earning.amount)
            })
            total_earning += earning.amount
            
        overtime_list = []
        total_overtime = Decimal('0.00')
        for ot in PayrollOvertime.objects.filter(payroll_result=payroll_result).select_related('overtime_type'):
            overtime_list.append({
                'name': ot.overtime_type.overtime_name,
                'multiplier' : str(ot.overtime_type.multiplier),
                'hours': str(ot.hours_worked),
                'amount': str(ot.amount)
            })
            total_overtime += ot.amount
            
        benefits = []
        total_benefits = Decimal('0.00')
        for benefit in PayrollBenefit.objects.filter(payroll_result=payroll_result).select_related('benefit_type'):
            benefits.append({
                'name': benefit.benefit_type.benefit_name,
                'amount': str(benefit.amount)
            })
            total_benefits += benefit.amount
            
        deductions = []
        total_deduction = Decimal('0.00')
        for deduction in PayrollDeduction.objects.filter(payroll_result=payroll_result).select_related('deduction_type'):
            deductions.append({
                'name': deduction.deduction_type.deduction_name,
                'taxable':deduction.deduction_type.is_taxable,
                'amount': str(deduction.amount)
            })
            total_deduction += deduction.amount 
            
        payslip = {
            'employee': {
                'id' : employee.id,
                'full_name': employee.full_name,
                'position': employee.position.position_name,
                'department': employee.department.department_name,
                'employment_status': employee.employment_status,
                'hire_date' : str(employee.hire_date)
            },
            'payrun': {
                'id': payrun.id,
                'start_date': str(payrun.start_date),
                'end_date': str(payrun.end_date),
                'pay_date': str(payrun.pay_date),
                'payroll_type': payrun.payroll_type
            },
            'earnings': earnings,
            'overtime': overtime_list,
            'benefits': benefits,
            'deductions': deductions,
            'summary': {
                'total_hours_worked': str(payroll_result.total_hours_worked),
                'total_earnings': str(total_earning), 
                'total_overtime': str(total_overtime),
                'total_benefits': str(total_benefits),
                'gross_pay': str(payroll_result.gross_pay),
                'total_deductions':str(payroll_result.total_deductions),
                'net_pay': str(payroll_result.net_pay),
                'generated_at': str(payroll_result.generate_at)
            }
        }
        
        return Response({'payslip': payslip},status=status.HTTP_200_OK)
    
class PayslipByPayrunView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request,payrun_id):
        try:
            payrun = PayRun.objects.get(pk = payrun_id)
        except PayRun.DoesNotExist:
            return Response({'error':'Payrun not found'},status=status.HTTP_404_NOT_FOUND)
        
        payroll_results = PayrollResult.objects.filter(payrun= payrun).select_related('employee','employee__position','employee__department')
        
        if not payroll_results.exists():
            return Response({'error': 'No payroll results found for this payrun. Please compute payroll first.'},status=status.HTTP_404_NOT_FOUND)
        
        payslips = []
        for payroll_result in payroll_results:
            employee = payroll_result.employee
            earnings = [{
            'name' : e.earning_type.earning_name,
            'amount': str(e.amount)
            }for e in PayrollEarning.objects.filter(payroll_result=payroll_result).select_related('earning_type')]
            
            overtime_list = [{
                'name': ot.overtime_type.overtime_name,
                'hours' : str(ot.hours_worked),
                'amount': str(ot.amount)
            }for ot in PayrollOvertime.objects.filter(payroll_result=payroll_result).select_related('overtime_type')]
            
            benefits = [{
                'name' : b.benefit_type.benefit_name,
                'amount' : str(b.amount) 
            }for b in PayrollBenefit.objects.filter(payroll_result=payroll_result).select_related('benefit_type')]
            
            deductions = [{
                'name': d.deduction_type.deduction_name,
                'amount': str(d.amount)
            } for d in PayrollDeduction.objects.filter(payroll_result=payroll_result).select_related('deduction_type')]
            
            payslips.append({
                'employee' : {
                    'id': employee.id,
                    'full_name' : employee.full_name,
                    'position': employee.position.position_name if employee.position else None,
                    'department': employee.department.department_name if employee.department else None,
                    'employment_status' : employee.employment_status
                },
                'earnings': earnings,
                'overtime' : overtime_list,
                'benefits' : benefits,
                'deductions' : deductions,
                'summary': {
                    'total_hours_worked' : str(payroll_result.total_hours_worked),
                    'gross_pay': str(payroll_result.gross_pay),
                    'total_deductions': str(payroll_result.total_deductions),
                    'net_pay': str(payroll_result.net_pay),
                }
            })
        return Response({
            'payrun' :{
                'id' : payrun.id,
                'start_date': str(payrun.start_date),
                'end_date': str(payrun.end_date),
                'pay_date': str(payrun.pay_date),
                'payroll_type' : str(payrun.payroll_type),
            },
            'total_employees': len(payslips),
            'payslips':payslips
        },status=status.HTTP_200_OK)
            