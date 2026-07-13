from django.test import TestCase
from decimal import Decimal
from datetime import date
from attendance.models import LeaveType, LeaveStatus, LeaveRequest, LeaveApproval, LeaveCredits
from attendance.services import process_leave_approval, reverse_leave_approval
from hr.models import Employee, Department, Position
from security.models import UserAccount, Role


class BaseAttendanceServiceTestCase(TestCase):

    def setUp(self):
        self.role = Role.objects.create(role_name='Staff', description='Staff Role')
        self.department = Department.objects.create(
            department_code='HR', department_name='Human Resources'
        )
        self.position = Position.objects.create(
            position_name='HR Officer', department=self.department
        )
        self.employee = Employee.objects.create(
            first_name='Jane',
            last_name='Smith',
            birth_date='1992-03-10',
            address='456 Office Ave',
            civil_status='SINGLE',
            phone_number='09987654321',
            personal_email='jane@test.com',
            employment_status='REGULAR',
            position=self.position,
            department=self.department,
            hire_date='2021-01-01',
            is_active=True,
        )
        self.approver = Employee.objects.create(
            first_name='Bob',
            last_name='Manager',
            birth_date='1985-05-15',
            address='789 Boss St',
            civil_status='MARRIED',
            phone_number='09111222333',
            personal_email='bob@test.com',
            employment_status='REGULAR',
            position=self.position,
            department=self.department,
            hire_date='2015-01-01',
            is_active=True,
        )
        self.leave_type = LeaveType.objects.create(
            leave_name='Vacation Leave',
            default_credits=Decimal('15.00'),
            is_paid=True,
            is_active=True,
        )
        self.pending_status = LeaveStatus.objects.create(
            leave_status_name='PENDING',
            description='Pending approval'
        )
        self.approved_status = LeaveStatus.objects.create(
            leave_status_name='APPROVED',
            description='Approved'
        )
        self.rejected_status = LeaveStatus.objects.create(
            leave_status_name='REJECTED',
            description='Rejected'
        )
        self.cancelled_status = LeaveStatus.objects.create(
            leave_status_name='CANCELLED',
            description='Cancelled'
        )
        self.leave_credits = LeaveCredits.objects.create(
            employee=self.employee,
            leave_type=self.leave_type,
            total_credits=Decimal('15.00'),
            used_credits=Decimal('0.00'),
            remaining_credits=Decimal('15.00'),
            year=2024,
        )
        self.leave_request = LeaveRequest.objects.create(
            employee=self.employee,
            leave_type=self.leave_type,
            leave_status=self.pending_status,
            start_date=date(2024, 6, 10),
            end_date=date(2024, 6, 10),
            leave_hours=Decimal('8.00'),
            reason='Rest day',
        )


# ─── process_leave_approval Tests ───────────────────────────────

class ProcessLeaveApprovalTests(BaseAttendanceServiceTestCase):

    def _create_approval(self):
        return LeaveApproval.objects.create(
            leave_request=self.leave_request,
            approved_by=self.approver,
            remarks='Approved',
            approved_at='2024-06-09T10:00:00Z',
        )

    def test_approval_deducts_used_credits(self):
        approval = self._create_approval()
        process_leave_approval(approval)
        self.leave_credits.refresh_from_db()
        self.assertEqual(self.leave_credits.used_credits, Decimal('1.00'))

    def test_approval_reduces_remaining_credits(self):
        approval = self._create_approval()
        process_leave_approval(approval)
        self.leave_credits.refresh_from_db()
        self.assertEqual(self.leave_credits.remaining_credits, Decimal('14.00'))

    def test_approval_sets_leave_request_to_approved(self):
        approval = self._create_approval()
        process_leave_approval(approval)
        self.leave_request.refresh_from_db()
        self.assertEqual(self.leave_request.leave_status.leave_status_name, 'APPROVED')

    def test_approval_returns_updated_leave_credits(self):
        approval = self._create_approval()
        result = process_leave_approval(approval)
        self.assertEqual(result.remaining_credits, Decimal('14.00'))

    def test_approval_with_half_day_deducts_half_credit(self):
        self.leave_request.leave_hours = Decimal('4.00')
        self.leave_request.save()
        approval = self._create_approval()
        process_leave_approval(approval)
        self.leave_credits.refresh_from_db()
        self.assertEqual(self.leave_credits.used_credits, Decimal('0.50'))
        self.assertEqual(self.leave_credits.remaining_credits, Decimal('14.50'))

    def test_approval_with_multi_day_leave(self):
        self.leave_request.leave_hours = Decimal('24.00')  # 3 days
        self.leave_request.save()
        approval = self._create_approval()
        process_leave_approval(approval)
        self.leave_credits.refresh_from_db()
        self.assertEqual(self.leave_credits.used_credits, Decimal('3.00'))
        self.assertEqual(self.leave_credits.remaining_credits, Decimal('12.00'))

    def test_approval_raises_error_when_insufficient_credits(self):
        self.leave_credits.remaining_credits = Decimal('0.00')
        self.leave_credits.save()
        approval = self._create_approval()
        with self.assertRaises(ValueError) as ctx:
            process_leave_approval(approval)
        self.assertIn('Insufficient', str(ctx.exception))

    def test_approval_does_not_deduct_when_insufficient(self):
        self.leave_credits.remaining_credits = Decimal('0.00')
        self.leave_credits.save()
        approval = self._create_approval()
        try:
            process_leave_approval(approval)
        except ValueError:
            pass
        self.leave_credits.refresh_from_db()
        self.assertEqual(self.leave_credits.used_credits, Decimal('0.00'))

    def test_approval_raises_error_when_no_leave_credits(self):
        self.leave_credits.delete()
        approval = self._create_approval()
        with self.assertRaises(ValueError) as ctx:
            process_leave_approval(approval)
        self.assertIn('No leave credits found', str(ctx.exception))

    def test_approval_raises_error_when_approved_status_missing(self):
        self.approved_status.delete()
        approval = self._create_approval()
        with self.assertRaises(ValueError) as ctx:
            process_leave_approval(approval)
        self.assertIn('APPROVED status not found', str(ctx.exception))

    def test_approval_total_credits_unchanged(self):
        approval = self._create_approval()
        process_leave_approval(approval)
        self.leave_credits.refresh_from_db()
        self.assertEqual(self.leave_credits.total_credits, Decimal('15.00'))

    def test_multiple_approvals_accumulate_deductions(self):
        # First approval
        approval1 = self._create_approval()
        process_leave_approval(approval1)

        # Second leave request
        leave_request2 = LeaveRequest.objects.create(
            employee=self.employee,
            leave_type=self.leave_type,
            leave_status=self.pending_status,
            start_date=date(2024, 6, 12),
            end_date=date(2024, 6, 12),
            leave_hours=Decimal('8.00'),
            reason='Another rest day',
        )
        approval2 = LeaveApproval.objects.create(
            leave_request=leave_request2,
            approved_by=self.approver,
            remarks='Approved',
            approved_at='2024-06-11T10:00:00Z',
        )
        process_leave_approval(approval2)

        self.leave_credits.refresh_from_db()
        self.assertEqual(self.leave_credits.used_credits, Decimal('2.00'))
        self.assertEqual(self.leave_credits.remaining_credits, Decimal('13.00'))


# ─── reverse_leave_approval Tests ───────────────────────────────

class ReverseLeaveApprovalTests(BaseAttendanceServiceTestCase):

    def setUp(self):
        super().setUp()
        # Create and process an approval first
        self.approval = LeaveApproval.objects.create(
            leave_request=self.leave_request,
            approved_by=self.approver,
            remarks='Approved',
            approved_at='2024-06-09T10:00:00Z',
        )
        process_leave_approval(self.approval)
        # Refresh to get updated credits
        self.leave_credits.refresh_from_db()

    def test_reversal_restores_used_credits(self):
        reverse_leave_approval(self.approval)
        self.leave_credits.refresh_from_db()
        self.assertEqual(self.leave_credits.used_credits, Decimal('0.00'))

    def test_reversal_restores_remaining_credits(self):
        reverse_leave_approval(self.approval)
        self.leave_credits.refresh_from_db()
        self.assertEqual(self.leave_credits.remaining_credits, Decimal('15.00'))

    def test_reversal_sets_leave_request_to_pending(self):
        reverse_leave_approval(self.approval)
        self.leave_request.refresh_from_db()
        self.assertEqual(self.leave_request.leave_status.leave_status_name, 'PENDING')

    def test_reversal_returns_updated_leave_credits(self):
        result = reverse_leave_approval(self.approval)
        self.assertEqual(result.remaining_credits, Decimal('15.00'))

    def test_reversal_raises_error_when_no_leave_credits(self):
        self.leave_credits.delete()
        with self.assertRaises(ValueError) as ctx:
            reverse_leave_approval(self.approval)
        self.assertIn('No leave credits found', str(ctx.exception))

    def test_reversal_raises_error_when_pending_status_missing(self):
        self.pending_status.delete()
        with self.assertRaises(ValueError) as ctx:
            reverse_leave_approval(self.approval)
        self.assertIn('PENDING status not found', str(ctx.exception))

    def test_reversal_total_credits_unchanged(self):
        reverse_leave_approval(self.approval)
        self.leave_credits.refresh_from_db()
        self.assertEqual(self.leave_credits.total_credits, Decimal('15.00'))

    def test_approve_then_reverse_returns_to_original_state(self):
        reverse_leave_approval(self.approval)
        self.leave_credits.refresh_from_db()
        self.assertEqual(self.leave_credits.used_credits, Decimal('0.00'))
        self.assertEqual(self.leave_credits.remaining_credits, Decimal('15.00'))
        self.leave_request.refresh_from_db()
        self.assertEqual(self.leave_request.leave_status.leave_status_name, 'PENDING')