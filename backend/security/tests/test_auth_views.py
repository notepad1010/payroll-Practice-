from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, timedelta
from security.models import UserAccount, PasswordResetRequest, TwoFactorCode
from hr.models import Employee, Position, Department
from security.models import Role
import hashlib


class BaseAuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.role = Role.objects.create(
            role_name='Test Role',
            description='Test role'
        )
        self.department = Department.objects.create(
            department_code='IT',
            department_name='Information Technology'
        )
        self.position = Position.objects.create(
            position_name='Developer',
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
            username='testuser',
            email='testuser@test.com',
            company_email='test.user@company.com',
            password='testpass123',
            employee=self.employee,
            role=self.role
        )


# ─── Login Tests ───────────────────────────────────────

class LoginViewTests(BaseAuthTestCase):

    URL = '/api/security/login/'

    def test_login_valid_credentials_returns_200(self):
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_password_returns_400(self):
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_invalid_username_returns_400(self):
        data = {'username': 'nonexistent', 'password': 'testpass123'}
        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_fields_returns_400(self):
        response = self.client.post(self.URL, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_locked_account_returns_400(self):
        self.user.is_locked = True
        self.user.save()
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_returns_valid_token_format(self):
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Tokens should be non-empty strings
        self.assertTrue(len(response.data['access']) > 0)
        self.assertTrue(len(response.data['refresh']) > 0)


# ─── Logout Tests ───────────────────────────────────────

class LogoutViewTests(BaseAuthTestCase):

    URL = '/api/security/logout/'

    def get_tokens(self):
        response = self.client.post('/api/security/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        return response.data['access'], response.data['refresh']

    def test_logout_valid_token_returns_200(self):
        access, refresh = self.get_tokens()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        response = self.client.post(self.URL, {'refresh': refresh}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_logout_without_refresh_token_returns_400(self):
        access, _ = self.get_tokens()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        response = self.client.post(self.URL, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_unauthenticated_returns_401(self):
        response = self.client.post(self.URL, {'refresh': 'sometoken'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_invalid_refresh_token_returns_400(self):
        access, _ = self.get_tokens()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        response = self.client.post(self.URL, {'refresh': 'invalidtoken'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_blacklists_token(self):
        access, refresh = self.get_tokens()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        # First logout
        self.client.post(self.URL, {'refresh': refresh}, format='json')
        # Try to use the same refresh token again
        response = self.client.post(self.URL, {'refresh': refresh}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ─── Change Password Tests ───────────────────────────────────────

class ChangePasswordViewTests(BaseAuthTestCase):

    URL = '/api/security/change-password/'

    def setUp(self):
        super().setUp()
        login = self.client.post('/api/security/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {login.data["access"]}'
        )

    def test_change_password_valid_data_returns_200(self):
        data = {
            'old_password': 'testpass123',
            'new_password': 'newpass456',
            'confirm_password': 'newpass456'
        }
        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password_updates_password(self):
        data = {
            'old_password': 'testpass123',
            'new_password': 'newpass456',
            'confirm_password': 'newpass456'
        }
        self.client.post(self.URL, data, format='json')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass456'))

    def test_change_password_wrong_old_password_returns_400(self):
        data = {
            'old_password': 'wrongpassword',
            'new_password': 'newpass456',
            'confirm_password': 'newpass456'
        }
        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_mismatched_new_passwords_returns_400(self):
        data = {
            'old_password': 'testpass123',
            'new_password': 'newpass456',
            'confirm_password': 'differentpass'
        }
        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_unauthenticated_returns_401(self):
        self.client.credentials()
        data = {
            'old_password': 'testpass123',
            'new_password': 'newpass456',
            'confirm_password': 'newpass456'
        }
        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_password_too_short_returns_400(self):
        data = {
            'old_password': 'testpass123',
            'new_password': 'short',
            'confirm_password': 'short'
        }
        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ─── Password Reset Request Tests ───────────────────────────────────────

class PasswordResetRequestViewTests(BaseAuthTestCase):

    URL = '/api/security/password-reset/'

    def test_valid_company_email_returns_201(self):
        data = {'company_email': self.user.company_email}
        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('reset_request_id', response.data)
        self.assertIn('otp_dev_only', response.data)

    def test_invalid_email_returns_400(self):
        data = {'company_email': 'nonexistent@company.com'}
        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_email_returns_400(self):
        response = self.client.post(self.URL, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creates_reset_request_in_db(self):
        data = {'company_email': self.user.company_email}
        self.client.post(self.URL, data, format='json')
        self.assertTrue(
            PasswordResetRequest.objects.filter(
                user_account=self.user,
                request_status='PENDING'
            ).exists()
        )

    def test_creates_otp_in_db(self):
        data = {'company_email': self.user.company_email}
        response = self.client.post(self.URL, data, format='json')
        reset_id = response.data['reset_request_id']
        reset_request = PasswordResetRequest.objects.get(id=reset_id)
        self.assertTrue(
            TwoFactorCode.objects.filter(
                reset_request=reset_request,
                purpose='PASSWORD_RESET',
                is_used=False
            ).exists()
        )

    def test_otp_is_hashed_in_db(self):
        data = {'company_email': self.user.company_email}
        response = self.client.post(self.URL, data, format='json')
        plain_otp = response.data['otp_dev_only']
        two_factor = TwoFactorCode.objects.filter(
            user_account=self.user
        ).latest('create_at')
        expected_hash = hashlib.sha256(plain_otp.encode()).hexdigest()
        self.assertEqual(two_factor.otp_code_hash, expected_hash)

    def test_previous_pending_requests_cancelled(self):
        data = {'company_email': self.user.company_email}
        first = self.client.post(self.URL, data, format='json')
        first_id = first.data['reset_request_id']
        self.client.post(self.URL, data, format='json')
        first_request = PasswordResetRequest.objects.get(id=first_id)
        self.assertEqual(first_request.request_status, 'CANCELLED')


# ─── Password Reset Confirm Tests ───────────────────────────────────────

class PasswordResetConfirmViewTests(BaseAuthTestCase):

    URL = '/api/security/password-reset/confirm'

    def setUp(self):
        super().setUp()
        # Create a reset request and OTP
        self.reset_request = PasswordResetRequest.objects.create(
            user_account=self.user,
            request_status='PENDING',
            request_at=date.today()
        )
        self.otp = '123456'
        self.otp_hash = hashlib.sha256(self.otp.encode()).hexdigest()
        self.two_factor = TwoFactorCode.objects.create(
            user_account=self.user,
            reset_request=self.reset_request,
            otp_code_hash=self.otp_hash,
            purpose='PASSWORD_RESET',
            expired_at=date.today() + timedelta(days=1),
            used_at=date.today(),
            is_used=False,
            attemp_count=0
        )

    def test_valid_otp_with_new_password_returns_200(self):
        data = {
            'reset_request_id': self.reset_request.id,
            'otp': self.otp,
            'new_password': 'newpass456'
        }
        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_otp_updates_password(self):
        data = {
            'reset_request_id': self.reset_request.id,
            'otp': self.otp,
            'new_password': 'newpass456'
        }
        self.client.post(self.URL, data, format='json')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass456'))

    def test_valid_otp_marks_otp_as_used(self):
        data = {
            'reset_request_id': self.reset_request.id,
            'otp': self.otp,
            'new_password': 'newpass456'
        }
        self.client.post(self.URL, data, format='json')
        self.two_factor.refresh_from_db()
        self.assertTrue(self.two_factor.is_used)

    def test_valid_otp_marks_request_completed(self):
        data = {
            'reset_request_id': self.reset_request.id,
            'otp': self.otp,
            'new_password': 'newpass456'
        }
        self.client.post(self.URL, data, format='json')
        self.reset_request.refresh_from_db()
        self.assertEqual(self.reset_request.request_status, 'COMPLETED')

    def test_invalid_otp_returns_400(self):
        data = {
            'reset_request_id': self.reset_request.id,
            'otp': '000000',
            'new_password': 'newpass456'
        }
        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_otp_increments_attempt_count(self):
        data = {
            'reset_request_id': self.reset_request.id,
            'otp': '000000',
            'new_password': 'newpass456'
        }
        self.client.post(self.URL, data, format='json')
        self.two_factor.refresh_from_db()
        self.assertEqual(self.two_factor.attemp_count, 1)

    def test_invalid_reset_request_id_returns_400(self):
        data = {
            'reset_request_id': 99999,
            'otp': self.otp,
            'new_password': 'newpass456'
        }
        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_expired_otp_returns_400(self):
        self.two_factor.expired_at = date.today() - timedelta(days=1)
        self.two_factor.save()
        data = {
            'reset_request_id': self.reset_request.id,
            'otp': self.otp,
            'new_password': 'newpass456'
        }
        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.reset_request.refresh_from_db()
        self.assertEqual(self.reset_request.request_status, 'EXPIRED')

    def test_already_used_otp_returns_400(self):
        self.two_factor.is_used = True
        self.two_factor.save()
        data = {
            'reset_request_id': self.reset_request.id,
            'otp': self.otp,
            'new_password': 'newpass456'
        }
        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_max_attempts_locks_account(self):
        self.two_factor.attemp_count = 5
        self.two_factor.save()
        data = {
            'reset_request_id': self.reset_request.id,
            'otp': '000000',
            'new_password': 'newpass456'
        }
        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_locked)

    def test_without_new_password_still_marks_otp_used(self):
        data = {
            'reset_request_id': self.reset_request.id,
            'otp': self.otp,
        }
        response = self.client.post(self.URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.two_factor.refresh_from_db()
        self.assertTrue(self.two_factor.is_used)

    def test_empty_body_returns_400(self):
        response = self.client.post(self.URL, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)