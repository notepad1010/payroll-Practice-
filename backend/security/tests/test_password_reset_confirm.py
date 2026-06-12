from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, timedelta
from security.models import UserAccount, PasswordResetRequest, TwoFactorCode
from hr.models import Employee, Position, Department
from security.models import Role
import hashlib


class PasswordResetConfirmViewTest(TestCase):
    """Test cases for PasswordResetConfirmView"""

    def setUp(self):
        """Set up test data and client"""
        self.client = APIClient()
        
        # Create role
        self.role = Role.objects.create(
            role_name='Test Role',
            description='Test role for testing'
        )
        
        # Create department
        self.department = Department.objects.create(
            department_code='IT',
            department_name='Information Technology'
        )
        
        # Create position
        self.position = Position.objects.create(
            position_name='Developer',
            description='Software Developer',
            department=self.department
        )
        
        # Create employee
        self.employee = Employee.objects.create(
            first_name='Reset',
            last_name='User',
            birth_date='1993-01-01',
            address='321 Reset St',
            civil_status='SINGLE',
            phone_number='1111111111',
            personal_email='reset@test.com',
            employment_status='REGULAR',
            position=self.position,
            department=self.department,
            hire_date='2022-01-01'
        )
        
        # Create user
        self.user = UserAccount.objects.create_user(
            username='resetuser',
            email='resetuser@test.com',
            company_email='reset.user@company.com',
            password='testpass123',
            employee=self.employee,
            role=self.role
        )
        
        # Create a valid reset request
        self.reset_request = PasswordResetRequest.objects.create(
            user_account=self.user,
            request_status='PENDING',
            request_at=date.today()
        )
        
        # Create a valid OTP
        self.otp = '123456'
        self.otp_hash = hashlib.sha256(self.otp.encode()).hexdigest()
        self.two_factor = TwoFactorCode.objects.create(
            user_account=self.user,
            reset_request=self.reset_request,
            otp_code_hash=self.otp_hash,
            purpose='PASSWORD_RESET',
            expired_at=date.today() + timedelta(minutes=15),
            used_at=date.today(),
            is_used=False,
            attemp_count=0
        )
        
        self.url = '/api/security/password-reset/confirm'

    def test_valid_otp_with_password_reset(self):
        """Test password reset confirmation with valid OTP and new password"""
        data = {
            'reset_request_id': self.reset_request.id,
            'otp': self.otp,
            'new_password': 'newpass123'
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Password has been reset successfully.')
        
        # Verify password was changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass123'))
        
        # Verify OTP is marked as used
        self.two_factor.refresh_from_db()
        self.assertTrue(self.two_factor.is_used)
        
        # Verify reset request is marked as completed
        self.reset_request.refresh_from_db()
        self.assertEqual(self.reset_request.request_status, 'COMPLETED')

    def test_valid_otp_code_field(self):
        """Test password reset confirmation with 'otp_code' field instead of 'otp'"""
        data = {
            'reset_request_id': self.reset_request.id,
            'otp_code': self.otp,
            'new_password': 'newpass123'
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass123'))

    def test_invalid_otp(self):
        """Test password reset confirmation with invalid OTP"""
        data = {
            'reset_request_id': self.reset_request.id,
            'otp': '999999',
            'new_password': 'newpass123'
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid OTP.')
        
        # Verify attempt count increased
        self.two_factor.refresh_from_db()
        self.assertEqual(self.two_factor.attemp_count, 1)
        
        # Verify password was not changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('testpass123'))

    def test_missing_otp(self):
        """Test password reset confirmation without OTP"""
        data = {
            'reset_request_id': self.reset_request.id,
            'new_password': 'newpass123'
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Serializer returns non_field_errors for validation errors
        self.assertIn('non_field_errors', response.data)

    def test_missing_reset_request_id(self):
        """Test password reset confirmation without reset request ID"""
        data = {
            'otp': self.otp,
            'new_password': 'newpass123'
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_reset_request_id(self):
        """Test password reset confirmation with invalid reset request ID"""
        data = {
            'reset_request_id': 99999,
            'otp': self.otp,
            'new_password': 'newpass123'
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid or Expired reset request.')

    def test_expired_reset_request(self):
        """Test password reset confirmation with expired reset request"""
        # Create an expired reset request
        expired_request = PasswordResetRequest.objects.create(
            user_account=self.user,
            request_status='EXPIRED',
            request_at=date.today()
        )
        
        data = {
            'reset_request_id': expired_request.id,
            'otp': self.otp,
            'new_password': 'newpass123'
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid or Expired reset request.')

    def test_expired_otp_timeout(self):
        """Test password reset confirmation with expired OTP"""
        # Create a new reset request and OTP that is expired
        another_request = PasswordResetRequest.objects.create(
            user_account=self.user,
            request_status='PENDING',
            request_at=date.today()
        )
        
        expired_otp = '654321'
        expired_otp_hash = hashlib.sha256(expired_otp.encode()).hexdigest()
        expired_two_factor = TwoFactorCode.objects.create(
            user_account=self.user,
            reset_request=another_request,
            otp_code_hash=expired_otp_hash,
            purpose='PASSWORD_RESET',
            expired_at=date.today() - timedelta(days=1),  # Expired yesterday
            used_at=date.today(),
            is_used=False,
            attemp_count=0
        )
        
        data = {
            'reset_request_id': another_request.id,
            'otp': expired_otp,
            'new_password': 'newpass123'
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'OTP has expired. Please request a new one')
        
        # Verify reset request status is updated to EXPIRED
        another_request.refresh_from_db()
        self.assertEqual(another_request.request_status, 'EXPIRED')

    def test_otp_not_found(self):
        """Test password reset confirmation when OTP doesn't exist"""
        # Delete the two factor code
        self.two_factor.delete()
        
        data = {
            'reset_request_id': self.reset_request.id,
            'otp': self.otp,
            'new_password': 'newpass123'
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'OTP Not Found! or already used')

    def test_otp_already_used(self):
        """Test password reset confirmation when OTP is already used"""
        # Mark OTP as used
        self.two_factor.is_used = True
        self.two_factor.save()
        
        data = {
            'reset_request_id': self.reset_request.id,
            'otp': self.otp,
            'new_password': 'newpass123'
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'OTP Not Found! or already used')

    def test_max_attempt_exceeds_account_locked(self):
        """Test that account is locked after max failed attempts"""
        # Set attempt count to max
        self.two_factor.attemp_count = 5
        self.two_factor.save()
        
        data = {
            'reset_request_id': self.reset_request.id,
            'otp': '999999',  # Wrong OTP
            'new_password': 'newpass123'
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Too many failed attemp. Account is now Locked!')
        
        # Verify account is locked
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_locked)

    def test_multiple_failed_attempts_increment_counter(self):
        """Test that failed attempts increment the counter"""
        data = {
            'reset_request_id': self.reset_request.id,
            'otp': '000000',
            'new_password': 'newpass123'
        }
        
        # First attempt
        response1 = self.client.post(self.url, data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        
        self.two_factor.refresh_from_db()
        attempt_after_1 = self.two_factor.attemp_count
        
        # Second attempt
        response2 = self.client.post(self.url, data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        
        self.two_factor.refresh_from_db()
        attempt_after_2 = self.two_factor.attemp_count
        
        self.assertEqual(attempt_after_1, 1)
        self.assertEqual(attempt_after_2, 2)

    def test_password_reset_without_new_password(self):
        """Test password reset confirmation without providing new password"""
        data = {
            'reset_request_id': self.reset_request.id,
            'otp': self.otp
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify OTP is marked as used
        self.two_factor.refresh_from_db()
        self.assertTrue(self.two_factor.is_used)
        
        # Verify reset request is marked as completed
        self.reset_request.refresh_from_db()
        self.assertEqual(self.reset_request.request_status, 'COMPLETED')
        
        # Verify old password still works (no password change)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('testpass123'))

    def test_otp_used_at_timestamp_updated(self):
        """Test that used_at timestamp is updated when OTP is used"""
        data = {
            'reset_request_id': self.reset_request.id,
            'otp': self.otp,
            'new_password': 'newpass123'
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.two_factor.refresh_from_db()
        self.assertEqual(self.two_factor.used_at, date.today())

    def test_cancelled_reset_request(self):
        """Test password reset confirmation with cancelled reset request"""
        # Create a cancelled reset request
        cancelled_request = PasswordResetRequest.objects.create(
            user_account=self.user,
            request_status='CANCELLED',
            request_at=date.today()
        )
        
        data = {
            'reset_request_id': cancelled_request.id,
            'otp': self.otp,
            'new_password': 'newpass123'
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid or Expired reset request.')

    def test_valid_otp_after_failed_attempts(self):
        """Test that valid OTP works after failed attempts (but before max)"""
        # Make 2 failed attempts
        for _ in range(2):
            data = {
                'reset_request_id': self.reset_request.id,
                'otp': '000000',
                'new_password': 'newpass123'
            }
            self.client.post(self.url, data, format='json')
        
        # Now try with correct OTP
        correct_data = {
            'reset_request_id': self.reset_request.id,
            'otp': self.otp,
            'new_password': 'newpass456'
        }
        response = self.client.post(self.url, correct_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass456'))

    def test_empty_request_body(self):
        """Test password reset confirmation with empty request body"""
        data = {}
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_request_completed_status_set(self):
        """Test that reset request status is set to COMPLETED after successful reset"""
        initial_status = self.reset_request.request_status
        self.assertEqual(initial_status, 'PENDING')
        
        data = {
            'reset_request_id': self.reset_request.id,
            'otp': self.otp,
            'new_password': 'newpass123'
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.reset_request.refresh_from_db()
        self.assertEqual(self.reset_request.request_status, 'COMPLETED')

    def test_otp_hash_comparison(self):
        """Test that OTP hash is correctly compared"""
        # Create data with correct OTP
        data = {
            'reset_request_id': self.reset_request.id,
            'otp': self.otp,
            'new_password': 'newpass123'
        }
        
        # Hash should match
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Create new test data for failed hash comparison
        self.reset_request2 = PasswordResetRequest.objects.create(
            user_account=self.user,
            request_status='PENDING',
            request_at=date.today()
        )
        
        wrong_otp = '654321'
        wrong_otp_hash = hashlib.sha256(wrong_otp.encode()).hexdigest()
        
        self.two_factor2 = TwoFactorCode.objects.create(
            user_account=self.user,
            reset_request=self.reset_request2,
            otp_code_hash=wrong_otp_hash,
            purpose='PASSWORD_RESET',
            expired_at=date.today() + timedelta(minutes=15),
            used_at=date.today(),
            is_used=False,
            attemp_count=0
        )
        
        data2 = {
            'reset_request_id': self.reset_request2.id,
            'otp': '123456',  # Different OTP
            'new_password': 'newpass123'
        }
        
        response2 = self.client.post(self.url, data2, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
