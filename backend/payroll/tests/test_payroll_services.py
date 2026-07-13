from django.test import TestCase
from decimal import Decimal
from datetime import date
from hr.models import Employee, Department, Position, SalaryHistory, EmployeeBenefit, BenefitType
from attendance.models import Attendance
from contributions.models import (
    SSSContribution, PhilhealthContribution,
    PagIBIGContribution, WithHoldingTaxBracket
)
from payroll.models import (
    PayRun, PayrollResult, PayrollEarning,
    PayrollDeduction, PayrollOvertime, PayrollBenefit,
    DeductionType, EarningType, OvertimeType
)
from payroll.services import (
    calculate_sss, calculate_phihealth, calculate_pagibig,
    calculation_withhoding_tax, calculate_hours_worked,
    compute_payroll_for_employee, compute_payroll_for_payrun
)
from security.models import UserAccount, Role


class BasePayrollServiceTestCase(TestCase):

    def setUp(self):
        self.department = Department.objects.create(
            department_code='IT', department_name='IT Department'
        )
        self.position = Position.objects.create(
            position_name='Developer', department=self.department
        )
        self.employee = Employee.objects.create(
            first_name='John',
            last_name='Doe',
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
            end_date=None,
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
            description='Regular overtime',
        )
        self.deduction_type_sss = DeductionType.objects.create(
            deduction_name='SSS Contribution',
            is_taxable=False,
        )
        self.deduction_type_philhealth = DeductionType.objects.create(
            deduction_name='PhilHealth Contribution',
            is_taxable=False,
        )
        self.deduction_type_pagibig = DeductionType.objects.create(
            deduction_name='PagIBIG Contribution',
            is_taxable=False,
        )
        self.deduction_type_tax = DeductionType.objects.create(
            deduction_name='Withholding Tax',
            is_taxable=True,
        )
        # Seed SSS bracket
        self.sss_bracket = SSSContribution.objects.create(
            deduction_type=self.deduction_type_sss,
            min_salary=Decimal('20000.00'),
            max_salary=Decimal('40000.00'),
            base_tax=Decimal('900.00'),
            tax_rate=Decimal('4.50'),
            excess_over=Decimal('20000.00'),
            effective_start_date=date(2024, 1, 1),
        )
        # Seed PhilHealth bracket
        self.philhealth_bracket = PhilhealthContribution.objects.create(
            deduction_type=self.deduction_type_philhealth,
            premium_rate=Decimal('5.00'),
            salary_floor=Decimal('10000.00'),
            salary_ceiling=Decimal('80000.00'),
            employee_share_ratio=Decimal('0.5000'),
            employer_share_ratio=Decimal('0.5000'),
            effective_start_date=date(2024, 1, 1),
        )
        # Seed PagIBIG bracket
        self.pagibig_bracket = PagIBIGContribution.objects.create(
            deduction_type=self.deduction_type_pagibig,
            min_salary=Decimal('1000.00'),
            max_salary=Decimal('50000.00'),
            employee_share_rate=Decimal('2.00'),
            employer_share_rate=Decimal('2.00'),
            max_employee_share=Decimal('100.00'),
            max_employer_share=Decimal('100.00'),
            effective_start_date=date(2024, 1, 1),
        )
        # Seed withholding tax bracket
        self.tax_bracket = WithHoldingTaxBracket.objects.create(
            deduction_type=self.deduction_type_tax,
            min_salary=Decimal('20833.00'),
            max_salary=Decimal('33332.00'),
            base_tax=Decimal('1875.00'),
            tax_rate=Decimal('20.00'),
            excess_over=Decimal('20833.00'),
            effective_start_date=date(2024, 1, 1),
        )


# ─── Contribution Calculator Tests ───────────────────────────────

class CalculateSSSTests(BasePayrollServiceTestCase):

    def test_sss_calculated_correctly(self):
        result = calculate_sss(Decimal('30000.00'), date(2024, 6, 20))
        # base_tax(900) + (30000 - 20000) * 4.5 / 100 = 900 + 450 = 1350
        self.assertEqual(result, Decimal('1350.00'))

    def test_sss_returns_zero_when_no_bracket(self):
        result = calculate_sss(Decimal('999999.00'), date(2024, 6, 20))
        self.assertEqual(result, Decimal('0.00'))

    def test_sss_returns_zero_for_zero_salary(self):
        result = calculate_sss(Decimal('0.00'), date(2024, 6, 20))
        self.assertEqual(result, Decimal('0.00'))

    def test_sss_at_minimum_salary_of_bracket(self):
        result = calculate_sss(Decimal('20000.00'), date(2024, 6, 20))
        # base_tax(900) + (20000 - 20000) * 4.5 / 100 = 900
        self.assertEqual(result, Decimal('900.00'))

    def test_sss_at_maximum_salary_of_bracket(self):
        result = calculate_sss(Decimal('40000.00'), date(2024, 6, 20))
        # base_tax(900) + (40000 - 20000) * 4.5 / 100 = 900 + 900 = 1800
        self.assertEqual(result, Decimal('1800.00'))


class CalculatePhilHealthTests(BasePayrollServiceTestCase):

    def test_philhealth_calculated_correctly(self):
        result = calculate_phihealth(Decimal('30000.00'), date(2024, 6, 20))
        # 30000 * 5% * 0.5 = 750
        self.assertEqual(result, Decimal('750.00'))

    def test_philhealth_capped_at_ceiling(self):
        result = calculate_phihealth(Decimal('100000.00'), date(2024, 6, 20))
        # capped at 80000: 80000 * 5% * 0.5 = 2000
        self.assertEqual(result, Decimal('2000.00'))

    def test_philhealth_floored_at_floor(self):
        result = calculate_phihealth(Decimal('5000.00'), date(2024, 6, 20))
        # floored at 10000: 10000 * 5% * 0.5 = 250
        self.assertEqual(result, Decimal('250.00'))

    def test_philhealth_returns_zero_when_no_bracket(self):
        self.philhealth_bracket.delete()
        result = calculate_phihealth(Decimal('30000.00'), date(2024, 6, 20))
        self.assertEqual(result, Decimal('0.00'))


class CalculatePagIBIGTests(BasePayrollServiceTestCase):

    def test_pagibig_calculated_correctly(self):
        result = calculate_pagibig(Decimal('30000.00'), date(2024, 6, 20))
        # 30000 * 2% = 600, but capped at 100
        self.assertEqual(result, Decimal('100.00'))

    def test_pagibig_below_cap(self):
        result = calculate_pagibig(Decimal('3000.00'), date(2024, 6, 20))
        # 3000 * 2% = 60, under cap of 100
        self.assertEqual(result, Decimal('60.00'))

    def test_pagibig_returns_zero_when_no_bracket(self):
        result = calculate_pagibig(Decimal('999999.00'), date(2024, 6, 20))
        self.assertEqual(result, Decimal('0.00'))


class CalculateWithholdingTaxTests(BasePayrollServiceTestCase):

    def test_tax_calculated_correctly(self):
        result = calculation_withhoding_tax(Decimal('30000.00'), date(2024, 6, 20))
        # base_tax(1875) + (30000 - 20833) * 20% = 1875 + 1833.40 = 3708.40
        expected = Decimal('1875.00') + (Decimal('30000.00') - Decimal('20833.00')) * Decimal('20') / Decimal('100')
        self.assertEqual(result, expected.quantize(Decimal('0.01')))

    def test_tax_returns_zero_when_no_bracket(self):
        result = calculation_withhoding_tax(Decimal('999999.00'), date(2024, 6, 20))
        self.assertEqual(result, Decimal('0.00'))

    def test_tax_never_negative(self):
        result = calculation_withhoding_tax(Decimal('20833.00'), date(2024, 6, 20))
        self.assertGreaterEqual(result, Decimal('0.00'))


# ─── Hours Calculation Tests ───────────────────────────────

class CalculateHoursWorkedTests(BasePayrollServiceTestCase):

    def _make_attendance(self, status, time_in=None, time_out=None, overtime=0, work_date=None):
        from datetime import time
        return Attendance(
            employee=self.employee,
            work_date=work_date or date(2024, 6, 3),
            time_in=time_in,
            time_out=time_out,
            overtime_hours=Decimal(str(overtime)),
            attendance_status=status,
        )

    def test_present_with_times_calculates_hours(self):
        from datetime import time
        record = self._make_attendance(
            'PRESENT',
            time_in=time(8, 0),
            time_out=time(17, 0),
        )
        regular, overtime = calculate_hours_worked([record])
        self.assertEqual(regular, Decimal('8.00'))

    def test_absent_contributes_zero_hours(self):
        record = self._make_attendance('ABSENT')
        regular, overtime = calculate_hours_worked([record])
        self.assertEqual(regular, Decimal('0.00'))
        self.assertEqual(overtime, Decimal('0.00'))

    def test_half_day_contributes_four_hours(self):
        record = self._make_attendance('HALF_DAY')
        regular, overtime = calculate_hours_worked([record])
        self.assertEqual(regular, Decimal('4.00'))

    def test_present_without_times_assumes_standard_hours(self):
        record = self._make_attendance('PRESENT')
        regular, overtime = calculate_hours_worked([record])
        self.assertEqual(regular, Decimal('8.00'))

    def test_overtime_hours_accumulated(self):
        from datetime import time
        record = self._make_attendance(
            'PRESENT',
            time_in=time(8, 0),
            time_out=time(17, 0),
            overtime=2,
        )
        regular, overtime = calculate_hours_worked([record])
        self.assertEqual(overtime, Decimal('2.00'))

    def test_multiple_records_accumulate(self):
        from datetime import time
        records = [
            self._make_attendance('PRESENT', time(8, 0), time(17, 0), work_date=date(2024, 6, 3)),
            self._make_attendance('PRESENT', time(8, 0), time(17, 0), work_date=date(2024, 6, 4)),
            self._make_attendance('HALF_DAY', work_date=date(2024, 6, 5)),
            self._make_attendance('ABSENT', work_date=date(2024, 6, 6)),
        ]
        regular, overtime = calculate_hours_worked(records)
        self.assertEqual(regular, Decimal('20.00'))  # 8 + 8 + 4 + 0

    def test_empty_records_returns_zero(self):
        regular, overtime = calculate_hours_worked([])
        self.assertEqual(regular, Decimal('0.00'))
        self.assertEqual(overtime, Decimal('0.00'))


# ─── compute_payroll_for_employee Tests ───────────────────────────────

class ComputePayrollForEmployeeTests(BasePayrollServiceTestCase):

    def setUp(self):
        super().setUp()
        # Create attendance records for the payrun period
        from datetime import time
        for day in range(1, 16):  # June 1-15
            try:
                work_date = date(2024, 6, day)
                if work_date.weekday() < 5:  # Mon-Fri only
                    Attendance.objects.create(
                        employee=self.employee,
                        work_date=work_date,
                        time_in=time(8, 0),
                        time_out=time(17, 0),
                        overtime_hours=Decimal('0.00'),
                        attendance_status='PRESENT',
                    )
            except Exception:
                pass

    def test_creates_payroll_result(self):
        result = compute_payroll_for_employee(self.employee, self.payrun)
        self.assertIsInstance(result, PayrollResult)

    def test_payroll_result_linked_to_employee(self):
        result = compute_payroll_for_employee(self.employee, self.payrun)
        self.assertEqual(result.employee, self.employee)

    def test_payroll_result_linked_to_payrun(self):
        result = compute_payroll_for_employee(self.employee, self.payrun)
        self.assertEqual(result.payrun, self.payrun)

    def test_gross_pay_is_positive(self):
        result = compute_payroll_for_employee(self.employee, self.payrun)
        self.assertGreater(result.gross_pay, Decimal('0.00'))

    def test_net_pay_is_less_than_gross(self):
        result = compute_payroll_for_employee(self.employee, self.payrun)
        self.assertLess(result.net_pay, result.gross_pay)

    def test_total_deductions_is_positive(self):
        result = compute_payroll_for_employee(self.employee, self.payrun)
        self.assertGreater(result.total_deductions, Decimal('0.00'))

    def test_net_pay_equals_gross_minus_deductions(self):
        result = compute_payroll_for_employee(self.employee, self.payrun)
        expected_net = result.gross_pay - result.total_deductions
        self.assertEqual(result.net_pay, expected_net)

    def test_creates_earning_records(self):
        result = compute_payroll_for_employee(self.employee, self.payrun)
        self.assertTrue(PayrollEarning.objects.filter(payroll_result=result).exists())

    def test_creates_deduction_records(self):
        result = compute_payroll_for_employee(self.employee, self.payrun)
        self.assertTrue(PayrollDeduction.objects.filter(payroll_result=result).exists())

    def test_raises_error_when_no_salary(self):
        self.salary.delete()
        with self.assertRaises(ValueError) as ctx:
            compute_payroll_for_employee(self.employee, self.payrun)
        self.assertIn('No salary record found', str(ctx.exception))

    def test_recompute_deletes_old_result(self):
        compute_payroll_for_employee(self.employee, self.payrun)
        compute_payroll_for_employee(self.employee, self.payrun)
        count = PayrollResult.objects.filter(
            employee=self.employee, payrun=self.payrun
        ).count()
        self.assertEqual(count, 1)

    def test_overtime_creates_overtime_record(self):
        Attendance.objects.filter(
            employee=self.employee,
            work_date=date(2024, 6, 3)
        ).update(overtime_hours=Decimal('2.00'))
        result = compute_payroll_for_employee(self.employee, self.payrun)
        self.assertTrue(PayrollOvertime.objects.filter(payroll_result=result).exists())

    def test_benefit_creates_benefit_record(self):
        benefit_type = BenefitType.objects.create(
            benefit_name='Transportation Allowance',
            description='Monthly transportation'
        )
        EmployeeBenefit.objects.create(
            employee=self.employee,
            benefit=benefit_type,
            amount=Decimal('2000.00'),
            effective_start_date=date(2024, 1, 1),
        )
        result = compute_payroll_for_employee(self.employee, self.payrun)
        self.assertTrue(PayrollBenefit.objects.filter(payroll_result=result).exists())


# ─── compute_payroll_for_payrun Tests ───────────────────────────────

class ComputePayrollForPayrunTests(BasePayrollServiceTestCase):

    def setUp(self):
        super().setUp()
        from datetime import time
        Attendance.objects.create(
            employee=self.employee,
            work_date=date(2024, 6, 3),
            time_in=time(8, 0),
            time_out=time(17, 0),
            overtime_hours=Decimal('0.00'),
            attendance_status='PRESENT',
        )

    def test_returns_results_and_errors(self):
        results, errors = compute_payroll_for_payrun(self.payrun)
        self.assertIsInstance(results, list)
        self.assertIsInstance(errors, list)

    def test_processes_active_employees(self):
        results, errors = compute_payroll_for_payrun(self.payrun)
        total = len(results) + len(errors)
        active_count = Employee.objects.filter(is_active=True).count()
        self.assertEqual(total, active_count)

    def test_skips_inactive_employees(self):
        inactive = Employee.objects.create(
            first_name='Inactive',
            last_name='User',
            birth_date='1990-01-01',
            address='Nowhere',
            civil_status='SINGLE',
            phone_number='00000000000',
            personal_email='inactive@test.com',
            employment_status='REGULAR',
            position=self.position,
            department=self.department,
            hire_date='2020-01-01',
            is_active=False,
        )
        results, errors = compute_payroll_for_payrun(self.payrun)
        employee_ids = [r['employee_id'] for r in results] + \
                       [e['employee_id'] for e in errors]
        self.assertNotIn(inactive.id, employee_ids)

    def test_error_recorded_for_employee_without_salary(self):
        self.salary.delete()
        results, errors = compute_payroll_for_payrun(self.payrun)
        self.assertTrue(len(errors) > 0)
        self.assertEqual(errors[0]['employee_id'], self.employee.id)

    def test_result_contains_required_fields(self):
        results, errors = compute_payroll_for_payrun(self.payrun)
        if results:
            result = results[0]
            self.assertIn('employee_id', result)
            self.assertIn('employee_name', result)
            self.assertIn('gross_pay', result)
            self.assertIn('total_deductions', result)
            self.assertIn('net_pay', result)