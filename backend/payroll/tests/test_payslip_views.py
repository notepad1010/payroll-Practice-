from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, time
from decimal import Decimal
from security.models import UserAccount, Role
from hr.models import Employee, Department, Position, SalaryHistory, BenefitType, EmployeeBenefit
from attendance.models import Attendance
from contributions.models import (
    SSSContribution, PhilhealthContribution,
    PagIBIGContribution, WithHoldingTaxBracket
)
from payroll.models import (
    PayRun, PayrollResult, PayrollEarning,
    PayrollDeduction, PayrollOvertime,
    DeductionType, EarningType, OvertimeType
)
from payroll.services import compute_payroll_for_employee


class BasePayslipTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = UserAccount.objects.create_superuser(
            username='testuser',
            password='Test@1234',
            email='test@payroll.com',
            company_email='test@payroll.com'
        )
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'Test@1234'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.department = Department.objects.create(
            department_code='IT', department_name='IT Department'
        )
        self.position = Position.objects.create(
            position_name='Developer', department=self.department
        )
        self.employee = Employee.objects.create(
            first_name='John', last_name='Doe',
            birth_date='1990-01-15',
            address='123 Main St',
            civil_status='SINGLE',
            phone_number='09123456789',
            personal_email='john@test.com',
            employment_status='REGULAR',
            position=self.position,
            department=self.department,
            hire_date='2020-01-01',
            is_active=True,
        )
        self.salary = SalaryHistory.objects.create(
            employee=self.employee,
            basic_salary=Decimal('30000.00'),
            gross_semi_monthly=Decimal('15000.00'),
            hourly_rate=Decimal('187.50'),
            start_date=date(2020, 1, 1),
        )
        self.payrun = PayRun.objects.create(
            start_date=date(2024, 6, 1),
            end_date=date(2024, 6, 15),
            pay_date=date(2024, 6, 20),
            payroll_type='SEMI_MONTLY',
        )
        self.overtime_type = OvertimeType.objects.create(
            overtime_name='Regular OT',
            multiplier=Decimal('1.25'),
        )
        # Seed contributions
        deduction_sss = DeductionType.objects.create(
            deduction_name='SSS Contribution', is_taxable=False
        )
        deduction_phil = DeductionType.objects.create(
            deduction_name='PhilHealth Contribution', is_taxable=False
        )
        deduction_pag = DeductionType.objects.create(
            deduction_name='PagIBIG Contribution', is_taxable=False
        )
        deduction_tax = DeductionType.objects.create(
            deduction_name='Withholding Tax', is_taxable=True
        )
        SSSContribution.objects.create(
            deduction_type=deduction_sss,
            min_salary=Decimal('20000.00'),
            max_salary=Decimal('40000.00'),
            base_tax=Decimal('900.00'),
            tax_rate=Decimal('4.50'),
            excess_over=Decimal('20000.00'),
            effective_start_date=date(2024, 1, 1),
        )
        PhilhealthContribution.objects.create(
            deduction_type=deduction_phil,
            premium_rate=Decimal('5.00'),
            salary_floor=Decimal('10000.00'),
            salary_ceiling=Decimal('80000.00'),
            employee_share_ratio=Decimal('0.5000'),
            employer_share_ratio=Decimal('0.5000'),
            effective_start_date=date(2024, 1, 1),
        )
        PagIBIGContribution.objects.create(
            deduction_type=deduction_pag,
            min_salary=Decimal('1000.00'),
            max_salary=Decimal('50000.00'),
            employee_share_rate=Decimal('2.00'),
            employer_share_rate=Decimal('2.00'),
            max_employee_share=Decimal('100.00'),
            max_employer_share=Decimal('100.00'),
            effective_start_date=date(2024, 1, 1),
        )
        WithHoldingTaxBracket.objects.create(
            deduction_type=deduction_tax,
            min_salary=Decimal('20833.00'),
            max_salary=Decimal('33332.00'),
            base_tax=Decimal('1875.00'),
            tax_rate=Decimal('20.00'),
            excess_over=Decimal('20833.00'),
            effective_start_date=date(2024, 1, 1),
        )
        # Attendance for period
        for day in range(1, 16):
            work_date = date(2024, 6, day)
            if work_date.weekday() < 5:
                Attendance.objects.create(
                    employee=self.employee,
                    work_date=work_date,
                    time_in=time(8, 0),
                    time_out=time(17, 0),
                    overtime_hours=Decimal('0.00'),
                    attendance_status='PRESENT',
                )
        # Compute payroll
        self.payroll_result = compute_payroll_for_employee(
            self.employee, self.payrun
        )


# ─── PayslipView Tests ───────────────────────────────────────

class PayslipViewTests(BasePayslipTestCase):

    def url(self, payrun_id=None, employee_id=None):
        payrun_id = payrun_id or self.payrun.id
        employee_id = employee_id or self.employee.id
        return f'/api/payroll/payslip/{payrun_id}/employee/{employee_id}/'

    def test_returns_200(self):
        response = self.client.get(self.url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_response_has_payslip_key(self):
        response = self.client.get(self.url())
        self.assertIn('payslip', response.data)

    def test_payslip_has_employee_section(self):
        response = self.client.get(self.url())
        self.assertIn('employee', response.data['payslip'])

    def test_payslip_has_payrun_section(self):
        response = self.client.get(self.url())
        self.assertIn('payrun', response.data['payslip'])

    def test_payslip_has_earnings_section(self):
        response = self.client.get(self.url())
        self.assertIn('earnings', response.data['payslip'])

    def test_payslip_has_deductions_section(self):
        response = self.client.get(self.url())
        self.assertIn('deductions', response.data['payslip'])

    def test_payslip_has_summary_section(self):
        response = self.client.get(self.url())
        self.assertIn('summary', response.data['payslip'])

    def test_employee_section_has_correct_fields(self):
        response = self.client.get(self.url())
        employee = response.data['payslip']['employee']
        self.assertIn('id', employee)
        self.assertIn('full_name', employee)
        self.assertIn('position', employee)
        self.assertIn('department', employee)
        self.assertIn('employment_status', employee)
        self.assertIn('hire_date', employee)

    def test_employee_full_name_correct(self):
        response = self.client.get(self.url())
        self.assertEqual(
            response.data['payslip']['employee']['full_name'],
            'John Doe'
        )

    def test_employee_position_correct(self):
        response = self.client.get(self.url())
        self.assertEqual(
            response.data['payslip']['employee']['position'],
            'Developer'
        )

    def test_employee_department_correct(self):
        response = self.client.get(self.url())
        self.assertEqual(
            response.data['payslip']['employee']['department'],
            'IT Department'
        )

    def test_summary_has_required_fields(self):
        response = self.client.get(self.url())
        summary = response.data['payslip']['summary']
        self.assertIn('total_hours_worked', summary)
        self.assertIn('gross_pay', summary)
        self.assertIn('total_deductions', summary)
        self.assertIn('net_pay', summary)
        self.assertIn('generated_at', summary)

    def test_net_pay_is_correct(self):
        response = self.client.get(self.url())
        summary = response.data['payslip']['summary']
        gross = Decimal(summary['gross_pay'])
        deductions = Decimal(summary['total_deductions'])
        net = Decimal(summary['net_pay'])
        self.assertEqual(net, gross - deductions)

    def test_earnings_is_list(self):
        response = self.client.get(self.url())
        self.assertIsInstance(response.data['payslip']['earnings'], list)

    def test_deductions_is_list(self):
        response = self.client.get(self.url())
        self.assertIsInstance(response.data['payslip']['deductions'], list)

    def test_earnings_have_name_and_amount(self):
        response = self.client.get(self.url())
        for earning in response.data['payslip']['earnings']:
            self.assertIn('name', earning)
            self.assertIn('amount', earning)

    def test_deductions_have_name_and_amount(self):
        response = self.client.get(self.url())
        for deduction in response.data['payslip']['deductions']:
            self.assertIn('name', deduction)
            self.assertIn('amount', deduction)

    def test_payrun_dates_correct(self):
        response = self.client.get(self.url())
        payrun = response.data['payslip']['payrun']
        self.assertEqual(payrun['start_date'], '2024-06-01')
        self.assertEqual(payrun['end_date'], '2024-06-15')
        self.assertEqual(payrun['pay_date'], '2024-06-20')

    def test_nonexistent_payrun_returns_404(self):
        response = self.client.get(
            f'/api/payroll/payslip/99999/{self.employee.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_nonexistent_employee_returns_404(self):
        response = self.client.get(
        f'/api/payroll/payslip/{self.payrun.id}/employee/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_no_payroll_result_returns_404(self):
        new_payrun = PayRun.objects.create(
        start_date=date(2024, 7, 1),
        end_date=date(2024, 7, 15),
        pay_date=date(2024, 7, 20),
        payroll_type='SEMI_MONTLY',
    )
        response = self.client.get(
        f'/api/payroll/payslip/{new_payrun.id}/employee/{self.employee.id}/'
    )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('compute payroll first', response.data['error'])

    def test_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.get(
        f'/api/payroll/payslip/{self.payrun.id}/employee/{self.employee.id}/'
    )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_overtime_section_present(self):
        response = self.client.get(self.url())
        self.assertIn('overtime', response.data['payslip'])
        self.assertIsInstance(response.data['payslip']['overtime'], list)

    def test_benefits_section_present(self):
        response = self.client.get(self.url())
        self.assertIn('benefits', response.data['payslip'])
        self.assertIsInstance(response.data['payslip']['benefits'], list)

    def test_overtime_payslip_shows_overtime(self):
        # Add overtime to one attendance record
        Attendance.objects.filter(
            employee=self.employee,
            work_date=date(2024, 6, 3)
        ).update(overtime_hours=Decimal('2.00'))
        # Recompute
        compute_payroll_for_employee(self.employee, self.payrun)
        response = self.client.get(self.url())
        self.assertTrue(len(response.data['payslip']['overtime']) > 0)

    def test_benefit_shows_in_payslip(self):
        benefit_type = BenefitType.objects.create(
            benefit_name='Meal Allowance', description='Daily meal'
        )
        EmployeeBenefit.objects.create(
            employee=self.employee,
            benefit=benefit_type,
            amount=Decimal('1500.00'),
            effective_start_date=date(2024, 1, 1),
        )
        compute_payroll_for_employee(self.employee, self.payrun)
        response = self.client.get(self.url())
        self.assertTrue(len(response.data['payslip']['benefits']) > 0)


# ─── PayslipByPayrunView Tests ───────────────────────────────────────

class PayslipByPayrunViewTests(BasePayslipTestCase):

    def url(self, payrun_id=None):
        payrun_id = payrun_id or self.payrun.id
        return f'/api/payroll/payslip/{payrun_id}/'

    def test_returns_200(self):
        response = self.client.get(self.url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_response_has_payslips_key(self):
        response = self.client.get(self.url())
        self.assertIn('payslips', response.data)

    def test_response_has_payrun_key(self):
        response = self.client.get(self.url())
        self.assertIn('payrun', response.data)

    def test_response_has_total_employees(self):
        response = self.client.get(self.url())
        self.assertIn('total_employees', response.data)

    def test_total_employees_correct(self):
        response = self.client.get(self.url())
        self.assertEqual(response.data['total_employees'], 1)

    def test_payslips_is_list(self):
        response = self.client.get(self.url())
        self.assertIsInstance(response.data['payslips'], list)

    def test_each_payslip_has_employee(self):
        response = self.client.get(self.url())
        for payslip in response.data['payslips']:
            self.assertIn('employee', payslip)

    def test_each_payslip_has_summary(self):
        response = self.client.get(self.url())
        for payslip in response.data['payslips']:
            self.assertIn('summary', payslip)

    def test_each_payslip_has_earnings(self):
        response = self.client.get(self.url())
        for payslip in response.data['payslips']:
            self.assertIn('earnings', payslip)

    def test_each_payslip_has_deductions(self):
        response = self.client.get(self.url())
        for payslip in response.data['payslips']:
            self.assertIn('deductions', payslip)

    def test_nonexistent_payrun_returns_404(self):
        response = self.client.get(
        f'/api/payroll/payslip/99999/employee/{self.employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_payrun_with_no_results_returns_404(self):
        new_payrun = PayRun.objects.create(
            start_date=date(2024, 7, 1),
            end_date=date(2024, 7, 15),
            pay_date=date(2024, 7, 20),
            payroll_type='SEMI_MONTLY',
        )
        response = self.client.get(f'/api/payroll/payslip/{new_payrun.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.get(
        f'/api/payroll/payslip/{self.payrun.id}/employee/{self.employee.id}/'
    )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_multiple_employees_appear_in_payslips(self):
        # Create second employee with salary and attendance
        employee2 = Employee.objects.create(
            first_name='Jane', last_name='Smith',
            birth_date='1992-03-10',
            address='456 Ave',
            civil_status='SINGLE',
            phone_number='09987654321',
            personal_email='jane@test.com',
            employment_status='REGULAR',
            position=self.position,
            department=self.department,
            hire_date='2021-01-01',
            is_active=True,
        )
        SalaryHistory.objects.create(
            employee=employee2,
            basic_salary=Decimal('25000.00'),
            gross_semi_monthly=Decimal('12500.00'),
            hourly_rate=Decimal('156.25'),
            start_date=date(2021, 1, 1),
        )
        from datetime import time
        Attendance.objects.create(
            employee=employee2,
            work_date=date(2024, 6, 3),
            time_in=time(8, 0),
            time_out=time(17, 0),
            overtime_hours=Decimal('0.00'),
            attendance_status='PRESENT',
        )
        compute_payroll_for_employee(employee2, self.payrun)

        response = self.client.get(self.url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_employees'], 2)