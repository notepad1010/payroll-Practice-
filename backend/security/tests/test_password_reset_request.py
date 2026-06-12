from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, timedelta
from security.models import UserAccount, PasswordResetRequest, TwoFactorCode
from hr.models import Employee, Position, Department
from security.models import Role
import hashlib
import json


class PasswordResetRequestModelTest(TestCase):
    """Test cases for PasswordResetRequest model"""

    def setUp(self):
        """Set up test data"""
        self.role = Role.objects.create(
            role_name='Test Role',
            description='Test role for testing'
        )
        
        self.department = Department.objects.create(
            department_code='IT',
            department_name='Information Technology'
        )
        
        self.position = Position.objects.create(
            position_name='Developer',
            description='Software Developer',
            department=self.department
        )
        
        self.employee = Employee.objects.create(
            first_name='John',
            last_name='Doe',
            birth_date='1990-01-01',
            address='123 Test St',
            civil_status='SINGLE',
            phone_number='1234567890',
            personal_email='john@test.com',
            employment_status='REGULAR',
            position=self.position,
            department=self.department,
            hire_date='2020-01-01'
        )
        
        self.user = UserAccount.objects.create_user(
            username='johndoe',
            email='johndoe@test.com',
            company_email='john.doe@company.com',
            password='testpass123',
            employee=self.employee,
            role=self.role
        )

    def test_create_password_reset_request(self):
        """Test creating a password reset request"""
        reset_request = PasswordResetRequest.objects.create(
            user_account=self.user,
            request_status='PENDING',
            request_at=date.today()
        )
        
        self.assertEqual(reset_request.user_account, self.user)
        self.assertEqual(reset_request.request_status, 'PENDING')
        self.assertIsNone(reset_request.complete_at)
        self.assertIsNone(reset_request.resolved_by)

    def test_password_reset_request_status_choices(self):
        """Test that status choices are valid"""
        valid_statuses = ['PENDING', 'COMPLETED', 'EXPIRED', 'CANCELLED']
        
        for status_choice in valid_statuses:
            reset_request = PasswordResetRequest.objects.create(
                user_account=self.user,
                request_status=status_choice,
                request_at=date.today()
            )
            self.assertEqual(reset_request.request_status, status_choice)

    def test_password_reset_request_str(self):
        """Test string representation of PasswordResetRequest"""
        reset_request = PasswordResetRequest.objects.create(
            user_account=self.user,
            request_status='PENDING',
            request_at=date.today()
        )
        
        expected_str = f'reset request for {self.user.email}'
        self.assertEqual(str(reset_request), expected_str)

    def test_password_reset_request_timestamps(self):
        """Test that timestamps are set correctly"""
        reset_request = PasswordResetRequest.objects.create(
            user_account=self.user,
            request_status='PENDING',
            request_at=date.today()
        )
        
        self.assertIsNotNone(reset_request.create_at)
        self.assertIsNotNone(reset_request.update_at)

    def test_update_password_reset_request(self):
        """Test updating a password reset request"""
        reset_request = PasswordResetRequest.objects.create(
            user_account=self.user,
            request_status='PENDING',
            request_at=date.today()
        )
        
        reset_request.request_status = 'COMPLETED'
        reset_request.complete_at = date.today()
        reset_request.save()
        
        refreshed_request = PasswordResetRequest.objects.get(id=reset_request.id)
        self.assertEqual(refreshed_request.request_status, 'COMPLETED')
        self.assertEqual(refreshed_request.complete_at, date.today())

    def test_multiple_reset_requests_for_user(self):
        """Test that a user can have multiple reset requests"""
        request1 = PasswordResetRequest.objects.create(
            user_account=self.user,
            request_status='PENDING',
            request_at=date.today()
        )
        
        request2 = PasswordResetRequest.objects.create(
            user_account=self.user,
            request_status='CANCELLED',
            request_at=date.today()
        )
        
        user_requests = PasswordResetRequest.objects.filter(user_account=self.user)
        self.assertEqual(user_requests.count(), 2)


class PasswordResetRequestViewTest(TestCase):
    """Test cases for PasswordResetRequestView"""

    def setUp(self):
        """Set up test data and client"""
        self.client = APIClient()
        
        self.role = Role.objects.create(
            role_name='Test Role',
            description='Test role for testing'
        )
        
        self.department = Department.objects.create(
            department_code='IT',
            department_name='Information Technology'
        )
        
        self.position = Position.objects.create(
            position_name='Developer',
            description='Software Developer',
            department=self.department
        )
        
        self.employee = Employee.objects.create(
            first_name='Jane',
            last_name='Doe',
            birth_date='1992-01-01',
            address='456 Test Ave',
            civil_status='SINGLE',
            phone_number='9876543210',
            personal_email='jane@test.com',
            employment_status='REGULAR',
            position=self.position,
            department=self.department,
            hire_date='2021-01-01'
        )
        
        self.user = UserAccount.objects.create_user(
            username='janedoe',
            email='janedoe@test.com',
            company_email='jane.doe@company.com',
            password='testpass123',
            employee=self.employee,
            role=self.role
        )
        
        self.url = '/api/security/password-reset/'

    def test_password_reset_request_valid_email(self):
        """Test password reset request with valid company email"""
        data = {'company_email': self.user.company_email}
        response = self.client.post(self.url, data, format='json')
        
        # Check response status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check response data
        self.assertIn('message', response.data)
        self.assertIn('reset_request_id', response.data)
        self.assertIn('otp_dev_only', response.data)
        
        # Check that reset request was created
        reset_requests = PasswordResetRequest.objects.filter(user_account=self.user)
        self.assertEqual(reset_requests.count(), 1)
        self.assertEqual(reset_requests.first().request_status, 'PENDING')

    def test_password_reset_request_invalid_email(self):
        """Test password reset request with invalid company email"""
        data = {'company_email': 'nonexistent@company.com'}
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_reset_request_missing_email(self):
        """Test password reset request without email"""
        data = {}
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_reset_request_invalid_email_format(self):
        """Test password reset request with invalid email format"""
        data = {'company_email': 'not-an-email'}
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_previous_pending_requests(self):
        """Test that previous pending requests are cancelled"""
        # Create first reset request
        data = {'company_email': self.user.company_email}
        response1 = self.client.post(self.url, data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        first_request_id = response1.data['reset_request_id']
        
        # Create second reset request
        response2 = self.client.post(self.url, data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        
        # Check that first request is cancelled
        first_request = PasswordResetRequest.objects.get(id=first_request_id)
        self.assertEqual(first_request.request_status, 'CANCELLED')
        
        # Check that second request is pending
        second_request = PasswordResetRequest.objects.get(
            id=response2.data['reset_request_id']
        )
        self.assertEqual(second_request.request_status, 'PENDING')

    def test_otp_creation_on_reset_request(self):
        """Test that OTP is created when reset request is made"""
        data = {'company_email': self.user.company_email}
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        reset_request_id = response.data['reset_request_id']
        reset_request = PasswordResetRequest.objects.get(id=reset_request_id)
        
        # Check that TwoFactorCode was created
        otp_codes = TwoFactorCode.objects.filter(
            reset_request=reset_request,
            purpose='PASSWORD_RESET'
        )
        self.assertEqual(otp_codes.count(), 1)
        
        otp = otp_codes.first()
        self.assertEqual(otp.user_account, self.user)
        self.assertFalse(otp.is_used)

    def test_otp_is_hashed(self):
        """Test that OTP is hashed before saving"""
        data = {'company_email': self.user.company_email}
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        otp_plain = response.data['otp_dev_only']
        
        # Get the TwoFactorCode record
        two_factor = TwoFactorCode.objects.filter(
            user_account=self.user,
            purpose='PASSWORD_RESET'
        ).latest('create_at')
        
        # Hash the plain OTP and compare
        expected_hash = hashlib.sha256(otp_plain.encode()).hexdigest()
        self.assertEqual(two_factor.otp_code_hash, expected_hash)

    def test_otp_expiration_time(self):
        """Test that OTP expiration is set to 15 minutes from now"""
        data = {'company_email': self.user.company_email}
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        two_factor = TwoFactorCode.objects.filter(
            user_account=self.user,
            purpose='PASSWORD_RESET'
        ).latest('create_at')
        
        expected_expiration = date.today() + timedelta(minutes=15)
        self.assertEqual(two_factor.expired_at, expected_expiration)

    def test_otp_initial_attempt_count(self):
        """Test that OTP attempt count starts at 0"""
        data = {'company_email': self.user.company_email}
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        two_factor = TwoFactorCode.objects.filter(
            user_account=self.user,
            purpose='PASSWORD_RESET'
        ).latest('create_at')
        
        self.assertEqual(two_factor.attemp_count, 0)

    def test_otp_is_not_used_initially(self):
        """Test that OTP is_used flag is False initially"""
        data = {'company_email': self.user.company_email}
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        two_factor = TwoFactorCode.objects.filter(
            user_account=self.user,
            purpose='PASSWORD_RESET'
        ).latest('create_at')
        
        self.assertFalse(two_factor.is_used)


class TwoFactorCodeModelTest(TestCase):
    """Test cases for TwoFactorCode model"""

    def setUp(self):
        """Set up test data"""
        self.role = Role.objects.create(
            role_name='Test Role',
            description='Test role for testing'
        )
        
        self.department = Department.objects.create(
            department_code='IT',
            department_name='Information Technology'
        )
        
        self.position = Position.objects.create(
            position_name='Tester',
            description='QA Tester',
            department=self.department
        )
        
        self.employee = Employee.objects.create(
            first_name='Test',
            last_name='User',
            birth_date='1995-01-01',
            address='789 Test Blvd',
            civil_status='SINGLE',
            phone_number='5555555555',
            personal_email='test@test.com',
            employment_status='REGULAR',
            position=self.position,
            department=self.department,
            hire_date='2022-01-01'
        )
        
        self.user = UserAccount.objects.create_user(
            username='testuser',
            email='testuser@test.com',
            company_email='test.user@company.com',
            password='testpass123',
            employee=self.employee,
            role=self.role
        )
        
        self.reset_request = PasswordResetRequest.objects.create(
            user_account=self.user,
            request_status='PENDING',
            request_at=date.today()
        )

    def test_create_two_factor_code(self):
        """Test creating a two-factor code"""
        otp_hash = hashlib.sha256('123456'.encode()).hexdigest()
        
        two_factor = TwoFactorCode.objects.create(
            user_account=self.user,
            reset_request=self.reset_request,
            otp_code_hash=otp_hash,
            purpose='PASSWORD_RESET',
            expired_at=date.today() + timedelta(minutes=15),
            used_at=date.today(),
            is_used=False,
            attemp_count=0
        )
        
        self.assertEqual(two_factor.user_account, self.user)
        self.assertEqual(two_factor.reset_request, self.reset_request)
        self.assertEqual(two_factor.purpose, 'PASSWORD_RESET')
        self.assertFalse(two_factor.is_used)

    def test_two_factor_code_purposes(self):
        """Test that purpose choices are valid"""
        valid_purposes = ['LOGIN_2FA', 'PASSWORD_RESET']
        
        for purpose in valid_purposes:
            otp_hash = hashlib.sha256('123456'.encode()).hexdigest()
            two_factor = TwoFactorCode.objects.create(
                user_account=self.user,
                reset_request=self.reset_request,
                otp_code_hash=otp_hash,
                purpose=purpose,
                expired_at=date.today() + timedelta(minutes=15),
                used_at=date.today(),
                is_used=False,
                attemp_count=0
            )
            self.assertEqual(two_factor.purpose, purpose)

    def test_two_factor_code_str(self):
        """Test string representation of TwoFactorCode"""
        otp_hash = hashlib.sha256('123456'.encode()).hexdigest()
        two_factor = TwoFactorCode.objects.create(
            user_account=self.user,
            reset_request=self.reset_request,
            otp_code_hash=otp_hash,
            purpose='PASSWORD_RESET',
            expired_at=date.today() + timedelta(minutes=15),
            used_at=date.today(),
            is_used=False,
            attemp_count=0
        )
        
        expected_str = f' 2FA for {self.user.email} - PASSWORD_RESET'
        self.assertEqual(str(two_factor), expected_str)

    def test_two_factor_code_update_attempt_count(self):
        """Test updating attempt count for two-factor code"""
        otp_hash = hashlib.sha256('123456'.encode()).hexdigest()
        two_factor = TwoFactorCode.objects.create(
            user_account=self.user,
            reset_request=self.reset_request,
            otp_code_hash=otp_hash,
            purpose='PASSWORD_RESET',
            expired_at=date.today() + timedelta(minutes=15),
            used_at=date.today(),
            is_used=False,
            attemp_count=0
        )
        
        two_factor.attemp_count = 3
        two_factor.save()
        
        refreshed = TwoFactorCode.objects.get(id=two_factor.id)
        self.assertEqual(refreshed.attemp_count, 3)

    def test_two_factor_code_mark_as_used(self):
        """Test marking two-factor code as used"""
        otp_hash = hashlib.sha256('123456'.encode()).hexdigest()
        two_factor = TwoFactorCode.objects.create(
            user_account=self.user,
            reset_request=self.reset_request,
            otp_code_hash=otp_hash,
            purpose='PASSWORD_RESET',
            expired_at=date.today() + timedelta(minutes=15),
            used_at=date.today(),
            is_used=False,
            attemp_count=0
        )
        
        two_factor.is_used = True
        two_factor.used_at = date.today()
        two_factor.save()
        
        refreshed = TwoFactorCode.objects.get(id=two_factor.id)
        self.assertTrue(refreshed.is_used)
        self.assertEqual(refreshed.used_at, date.today())
