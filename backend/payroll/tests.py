from rest_framework.test import APITestCase
from rest_framework import status
from security.models import UserAccount
from payroll.models.payrun import PayRun
from payroll.models.earning_type import EarningType
from payroll.models.deduction_type import DeductionType
from payroll.models.overtime_type import OvertimeType
from hr.models import Department, Position, Employee
import datetime

class BaseTestCase(APITestCase):
    def setUp(self):
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
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )

        self.department = Department.objects.create(
            department_code='IT',
            department_name='IT Department',
            is_active=True
        )
        self.position = Position.objects.create(
            position_name='Developer',
            department=self.department,
            is_active=True
        )
        self.employee = Employee.objects.create(
            first_name='John',
            last_name='Doe',
            birth_date='1995-01-15',
            address='123 Main St',
            civil_status='SINGLE',
            phone_number='09123456789',
            personal_email='john@test.com',
            employment_status='REGULAR',
            position=self.position,
            department=self.department,
            hire_date='2024-01-01',
            is_active=True
        )

class PayRunTests(BaseTestCase):

    def test_get_all_payruns(self):
        response = self.client.get('/api/payroll/payrun/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_payrun(self):
        data = {
            'start_date': '2024-06-01',
            'end_date': '2024-06-15',
            'pay_date': '2024-06-20',
            'payroll_type': 'SEMI_MONTLY'
        }
        response = self.client.post(
            '/api/payroll/payrun/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_nonexistent_payrun(self):
        response = self.client.get('/api/payroll/payrun/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_payrun(self):
        payrun = PayRun.objects.create(
            start_date='2024-06-01',
            end_date='2024-06-15',
            pay_date='2024-06-20',
            payroll_type='SEMI_MONTLY'
        )
        data = {
            'start_date': '2024-07-01',
            'end_date': '2024-07-15',
            'pay_date': '2024-07-20',
            'payroll_type': 'MONTHLY'
        }
        response = self.client.put(
            f'/api/payroll/payrun/{payrun.id}/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class EarningTypeTests(BaseTestCase):

    def test_get_all_earning_types(self):
        response = self.client.get('/api/payroll/earning-type/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_earning_type(self):
        data = {
            'earning_name': 'Basic Salary',
            'is_taxable': True,
            'description': 'Monthly basic salary'
        }
        response = self.client.post(
            '/api/payroll/earning-type/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['earning_name'], 'Basic Salary')

    def test_create_earning_type_duplicate(self):
        EarningType.objects.create(
            earning_name='Basic Salary',
            is_taxable=True
        )
        data = {
            'earning_name': 'Basic Salary',
            'is_taxable': True,
            'description': 'Monthly basic salary'
        }
        response = self.client.post(
            '/api/payroll/earning-type/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_nonexistent_earning_type(self):
        response = self.client.get('/api/payroll/earning-type/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_earning_type(self):
        earning = EarningType.objects.create(
            earning_name='Basic Salary',
            is_taxable=True
        )
        data = {
            'earning_name': 'Basic Salary',
            'is_taxable': False,
            'description': 'Updated description'
        }
        response = self.client.put(
            f'/api/payroll/earning-type/{earning.id}/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class DeductionTypeTests(BaseTestCase):

    def test_get_all_deduction_types(self):
        response = self.client.get('/api/payroll/deduction-type/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_deduction_type(self):
        data = {
            'deduction_name': 'SSS',
            'is_taxable': True,
            'description': 'Social Security System'
        }
        response = self.client.post(
            '/api/payroll/deduction-type/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['deduction_name'], 'SSS')

    def test_create_deduction_type_duplicate(self):
        DeductionType.objects.create(
            deduction_name='SSS',
            is_taxable=True
        )
        data = {
            'deduction_name': 'SSS',
            'is_taxable': True,
            'description': 'Social Security System'
        }
        response = self.client.post(
            '/api/payroll/deduction-type/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_nonexistent_deduction_type(self):
        response = self.client.get('/api/payroll/deduction-type/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class OvertimeTypeTests(BaseTestCase):

    def test_get_all_overtime_types(self):
        response = self.client.get('/api/payroll/overtime-list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_overtime_type(self):
        data = {
            'overtime_name': 'Regular OT',
            'multiplier': 1.25,
            'description': 'Regular overtime at 1.25x rate'
        }
        response = self.client.post(
            '/api/payroll/overtime-list/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_nonexistent_overtime_type(self):
        response = self.client.get('/api/payroll/overtime-list/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class PayrollResultTests(BaseTestCase):

    def test_get_all_payroll_results(self):
        response = self.client.get('/api/payroll/payroll-result/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistent_payroll_result(self):
        response = self.client.get('/api/payroll/payroll-result/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class PayrollEarningTests(BaseTestCase):

    def test_get_all_payroll_earnings(self):
        response = self.client.get('/api/payroll/payroll-earning/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistent_payroll_earning(self):
        response = self.client.get('/api/payroll/payroll-earning/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class PayrollDeductionTests(BaseTestCase):

    def test_get_all_payroll_deductions(self):
        response = self.client.get('/api/payroll/payroll-deduction/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistent_payroll_deduction(self):
        response = self.client.get('/api/payroll/payroll-deduction/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class PayrollOvertimeTests(BaseTestCase):

    def test_get_all_payroll_overtimes(self):
        response = self.client.get('/api/payroll/payroll-overtime/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistent_payroll_overtime(self):
        response = self.client.get('/api/payroll/payroll-overtime/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class PayrollBenefitTests(BaseTestCase):

    def test_get_all_payroll_benefits(self):
        response = self.client.get('/api/payroll/payroll-benefit/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistent_payroll_benefit(self):
        response = self.client.get('/api/payroll/payroll-benefit/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
