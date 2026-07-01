from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from payroll.models import PayrollResult,PayRun
from payroll.serializers import  PayrollResultSerializer
from payroll.services import compute_payroll_for_employee,compute_payroll_for_payrun
from hr.models import Employee


class ComputePayrollView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request,payrun_id):
        try:
            payrun = PayRun.objects.get(pk = payrun_id)
        except PayRun.DoesNotExist:
            return Response(
                {'error' : 'PayRun not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        results, errors = compute_payroll_for_payrun(payrun)
        
        return Response ({
            'payrun_id' : payrun_id,
            'start_date' : str(payrun.start_date),
            'end_date' : str(payrun.end_date),
            'pay_date' : str(payrun.pay_date),
            'total_processed' : len(results),
            'total_errors' : len(errors),
            'results' : results,
            'error' : errors,
        },status=status.HTTP_200_OK)
        
class ComputePayrollEmployeeView(APIView):
    
    permission_classes = [ IsAuthenticated]
    
    def post(self,request, payrun_id, employee_id):
        try:
            payrun = PayRun.objects.get(pk = payrun_id)
        except PayRun.DoesNotExist:
            return Response({'error': 'Payrun not found!'},
                    status=status.HTTP_404_NOT_FOUND)
            
        try: 
            employee = Employee.objects.get(pk = employee_id)
        except Employee.DoesNotExist:
            return Response({'error' : 'Employee not Found!'},
                            status=status.HTTP_404_NOT_FOUND)
        
        try:
            result = compute_payroll_for_employee(employee,payrun)
            return Response({
                'employee_id' : employee.id,
                'employee_name' : employee.full_name,
                'payrun_id': payrun_id,
                'total_hours_worked': str(result.total_hours_worked),
                'gross_pay': str(result.gross_pay),
                'total_deduction' : str(result.total_deductions),
                'net_pay': str(result.net_pay),
                'earnings' : PayrollResultSerializer(result).data.get('earnings',[])
                
                
            },status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            return Response(
                {'error' : f'Computation failed : {str(e)}'},
                 status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PayrollResultByPayrunView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,payrun_id):
        try:
            payrun = PayRun.objects.get(pk = payrun_id)
        except PayRun.DoesNotExist:
            return Response({
                'error' : 'Payrun not found'
            },status = status.HTTP_404_NOT_FOUND)
            
        results = PayrollResult.objects.filter(payrun=payrun).select_related('employee')
        
        data = [{
            'employee_id': r.employee.id,
            'employee_name' : r.employee.full_name,
            'total_worked_hours' : str(r.total_hours_worked),
            'gross_pay' : str(r.gross_pay),
            'total_deduction' : str(r.total_deductions),
            'net_pay' : str(r.net_pay),
            'generated_at' : str(r.generate_at),
        }for r in results]
        
        return Response({
            'payrun_id' : payrun_id,
            'start_date': str(payrun.start_date),
            'end_date': str(payrun.end_date),
            'total_employee' : len(data),
            'results': data
        },status=status.HTTP_200_OK)