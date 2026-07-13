from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date
from decimal import Decimal
from security.models import UserAccount, Role
from hr.models import (
    Department, Position, Employee,
    GovernmentDetails, SalaryHistory,
    BenefitType, EmployeeBenefit
)


class BaseHRTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Create superuser for auth
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

        # Base data
        self.department = Department.objects.create(
            department_code='IT',
            department_name='Information Technology',
            is_active=True
        )
        self.position = Position.objects.create(
            position_name='Software Developer',
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


# ─── Department Tests ───────────────────────────────────────

class DepartmentTests(BaseHRTestCase):

    def test_get_all_departments(self):
        response = self.client.get('/api/hr/departments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_single_department(self):
        response = self.client.get(f'/api/hr/departments/{self.department.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['department_name'], 'Information Technology')

    def test_create_department(self):
        data = {
            'department_code': 'HR',
            'department_name': 'Human Resources',
            'is_active': True
        }
        response = self.client.post('/api/hr/departments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['department_name'], 'Human Resources')

    def test_create_department_duplicate_code_returns_400(self):
        data = {
            'department_code': 'IT',  # already exists
            'department_name': 'IT Duplicate',
            'is_active': True
        }
        response = self.client.post('/api/hr/departments/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_department_missing_fields_returns_400(self):
        response = self.client.post('/api/hr/departments/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_department(self):
        data = {
            'department_code': 'IT',
            'department_name': 'IT Department Updated',
            'is_active': True
        }
        response = self.client.put(f'/api/hr/departments/{self.department.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['department_name'], 'IT Department Updated')

    def test_delete_department(self):
        response = self.client.delete(f'/api/hr/departments/{self.department.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Department.objects.filter(id=self.department.id).exists())

    def test_get_nonexistent_department_returns_404(self):
        response = self.client.get('/api/hr/departments/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_department_returns_404(self):
        data = {'department_code': 'XX', 'department_name': 'Ghost', 'is_active': True}
        response = self.client.put('/api/hr/departments/99999/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_department_returns_404(self):
        response = self.client.delete('/api/hr/departments/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_request_returns_401(self):
        self.client.credentials()
        response = self.client.get('/api/hr/departments/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ─── Position Tests ───────────────────────────────────────

class PositionTests(BaseHRTestCase):

    def test_get_all_positions(self):
        response = self.client.get('/api/hr/positions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_single_position(self):
        response = self.client.get(f'/api/hr/positions/{self.position.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['position_name'], 'Software Developer')

    def test_create_position(self):
        data = {
            'position_name': 'Project Manager',
            'department': self.department.id,
            'is_active': True
        }
        response = self.client.post('/api/hr/positions/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['position_name'], 'Project Manager')

    def test_create_position_duplicate_name_returns_400(self):
        data = {
            'position_name': 'Software Developer',  # already exists
            'department': self.department.id,
            'is_active': True
        }
        response = self.client.post('/api/hr/positions/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_position_missing_fields_returns_400(self):
        response = self.client.post('/api/hr/positions/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_position(self):
        data = {
            'position_name': 'Senior Developer',
            'department': self.department.id,
            'is_active': True
        }
        response = self.client.put(f'/api/hr/positions/{self.position.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['position_name'], 'Senior Developer')

    def test_delete_position_deactivates(self):
        response = self.client.delete(f'/api/hr/positions/{self.position.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.position.refresh_from_db()
        self.assertFalse(self.position.is_active)

    def test_get_nonexistent_position_returns_404(self):
        response = self.client.get('/api/hr/positions/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_position_returns_404(self):
        data = {'position_name': 'Ghost', 'department': self.department.id, 'is_active': True}
        response = self.client.put('/api/hr/positions/99999/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_request_returns_401(self):
        self.client.credentials()
        response = self.client.get('/api/hr/positions/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ─── Employee Tests ───────────────────────────────────────

class EmployeeTests(BaseHRTestCase):

    def test_get_all_employees(self):
        response = self.client.get('/api/hr/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_single_employee(self):
        response = self.client.get(f'/api/hr/employees/{self.employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')

    def test_create_employee(self):
        data = {
            'first_name': 'Maria',
            'last_name': 'Santos',
            'birth_date': '1998-05-20',
            'address': '456 Oak St',
            'civil_status': 'SINGLE',
            'phone_number': '09987654321',
            'personal_email': 'maria@test.com',
            'employment_status': 'PROBATIONARY',
            'position': self.position.id,
            'department': self.department.id,
            'hire_date': '2024-06-01',
            'is_active': True
        }
        response = self.client.post('/api/hr/employees/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'Maria')

    def test_create_employee_missing_fields_returns_400(self):
        response = self.client.post('/api/hr/employees/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_employee(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe Updated',
            'birth_date': '1995-01-15',
            'address': '123 Main St',
            'civil_status': 'MARRIED',
            'phone_number': '09123456789',
            'personal_email': 'john@test.com',
            'employment_status': 'REGULAR',
            'position': self.position.id,
            'department': self.department.id,
            'hire_date': '2024-01-01',
            'is_active': True
        }
        response = self.client.put(f'/api/hr/employees/{self.employee.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['last_name'], 'Doe Updated')

    def test_delete_employee_deactivates(self):
        response = self.client.delete(f'/api/hr/employees/{self.employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertFalse(self.employee.is_active)

    def test_get_nonexistent_employee_returns_404(self):
        response = self.client.get('/api/hr/employees/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_employee_returns_404(self):
        data = {
            'first_name': 'Ghost',
            'last_name': 'User',
            'birth_date': '1990-01-01',
            'address': 'Nowhere',
            'civil_status': 'SINGLE',
            'phone_number': '00000000000',
            'personal_email': 'ghost@test.com',
            'employment_status': 'REGULAR',
            'position': self.position.id,
            'department': self.department.id,
            'hire_date': '2024-01-01',
            'is_active': True
        }
        response = self.client.put('/api/hr/employees/99999/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_request_returns_401(self):
        self.client.credentials()
        response = self.client.get('/api/hr/employees/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_inactive_employees_not_in_list(self):
        self.employee.is_active = False
        self.employee.save()
        response = self.client.get('/api/hr/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [e['id'] for e in response.data]
        self.assertNotIn(self.employee.id, ids)


# ─── GovernmentDetails Tests ───────────────────────────────────────

class GovernmentDetailsTests(BaseHRTestCase):

    def setUp(self):
        super().setUp()
        self.gov_details = GovernmentDetails.objects.create(
            employee=self.employee,
            sss_number='12-3456789-0',
            tin_number='123-456-789-000',
            pagibig_number='1234-5678-9012',
            philhealth_number='12-345678901-2'
        )

    def test_get_all_government_details(self):
        response = self.client.get('/api/hr/government/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_single_government_details(self):
        response = self.client.get(f'/api/hr/goverment/{self.gov_details.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['sss_number'], '12-3456789-0')

    def test_create_government_details(self):
        new_employee = Employee.objects.create(
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
            hire_date='2024-01-01',
            is_active=True
        )
        data = {
            'employee': new_employee.id,
            'sss_number': '99-9999999-9',
            'tin_number': '999-999-999-000',
            'pagibig_number': '9999-9999-9999',
            'philhealth_number': '99-999999999-9'
        }
        response = self.client.post('/api/hr/government/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['sss_number'], '99-9999999-9')

    def test_create_duplicate_sss_returns_400(self):
        new_employee = Employee.objects.create(
            first_name='Bob',
            last_name='Jones',
            birth_date='1990-01-01',
            address='789 Side St',
            civil_status='SINGLE',
            phone_number='09111222333',
            personal_email='bob@test.com',
            employment_status='REGULAR',
            position=self.position,
            department=self.department,
            hire_date='2024-01-01',
            is_active=True
        )
        data = {
            'employee': new_employee.id,
            'sss_number': '12-3456789-0',  # duplicate
            'tin_number': '000-000-000-000',
            'pagibig_number': '0000-0000-0000',
            'philhealth_number': '00-000000000-0'
        }
        response = self.client.post('/api/hr/government/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_government_details(self):
        data = {
            'employee': self.employee.id,
            'sss_number': '12-3456789-0',
            'tin_number': '999-999-999-001',
            'pagibig_number': '1234-5678-9012',
            'philhealth_number': '12-345678901-2'
        }
        response = self.client.put(f'/api/hr/goverment/{self.gov_details.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tin_number'], '999-999-999-001')

    def test_delete_government_details(self):
        response = self.client.delete(f'/api/hr/goverment/{self.gov_details.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(GovernmentDetails.objects.filter(id=self.gov_details.id).exists())

    def test_get_nonexistent_government_details_returns_404(self):
        response = self.client.get('/api/hr/goverment/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_request_returns_401(self):
        self.client.credentials()
        response = self.client.get('/api/hr/government/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ─── SalaryHistory Tests ───────────────────────────────────────

class SalaryHistoryTests(BaseHRTestCase):

    def setUp(self):
        super().setUp()
        self.salary = SalaryHistory.objects.create(
            employee=self.employee,
            basic_salary=Decimal('30000.00'),
            gross_semi_monthly=Decimal('15000.00'),
            hourly_rate=Decimal('187.50'),
            start_date=date(2024, 1, 1),
            end_date=None
        )

    def test_get_all_salary_history(self):
        response = self.client.get('/api/hr/salary-history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_single_salary_history(self):
        response = self.client.get(f'/api/hr/salary-history/{self.salary.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['basic_salary'], '30000.00')

    def test_create_salary_history(self):
        data = {
            'employee': self.employee.id,
            'basic_salary': '35000.00',
            'gross_semi_monthly': '17500.00',
            'hourly_rate': '218.75',
            'start_date': '2025-01-01',
        }
        response = self.client.post('/api/hr/salary-history/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['basic_salary'], '35000.00')

    def test_create_salary_history_missing_fields_returns_400(self):
        response = self.client.post('/api/hr/salary-history/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_salary_history(self):
        data = {
            'employee': self.employee.id,
            'basic_salary': '32000.00',
            'gross_semi_monthly': '16000.00',
            'hourly_rate': '200.00',
            'start_date': '2024-01-01',
        }
        response = self.client.put(f'/api/hr/salary-history/{self.salary.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['basic_salary'], '32000.00')

    def test_delete_salary_history(self):
        response = self.client.delete(f'/api/hr/salary-history/{self.salary.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(SalaryHistory.objects.filter(id=self.salary.id).exists())

    def test_get_nonexistent_salary_history_returns_404(self):
        response = self.client.get('/api/hr/salary-history/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_salary_history_returns_404(self):
        data = {
            'employee': self.employee.id,
            'basic_salary': '32000.00',
            'gross_semi_monthly': '16000.00',
            'hourly_rate': '200.00',
            'start_date': '2024-01-01',
        }
        response = self.client.put('/api/hr/salary-history/99999/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_request_returns_401(self):
        self.client.credentials()
        response = self.client.get('/api/hr/salary-history/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ─── BenefitType Tests ───────────────────────────────────────

class BenefitTypeTests(BaseHRTestCase):

    def setUp(self):
        super().setUp()
        self.benefit_type = BenefitType.objects.create(
            benefit_name='Transportation Allowance',
            description='Monthly transportation benefit'
        )

    def test_get_all_benefit_types(self):
        response = self.client.get('/api/hr/benefit-type/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_single_benefit_type(self):
        response = self.client.get(f'/api/hr/benefit-type/{self.benefit_type.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['benefit_name'], 'Transportation Allowance')

    def test_create_benefit_type(self):
        data = {
            'benefit_name': 'Meal Allowance',
            'description': 'Daily meal allowance'
        }
        response = self.client.post('/api/hr/benefit-type/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['benefit_name'], 'Meal Allowance')

    def test_create_duplicate_benefit_type_returns_400(self):
        data = {
            'benefit_name': 'Transportation Allowance',  # duplicate
            'description': 'Another transport'
        }
        response = self.client.post('/api/hr/benefit-type/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_benefit_type_missing_fields_returns_400(self):
        response = self.client.post('/api/hr/benefit-type/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_benefit_type(self):
        data = {
            'benefit_name': 'Transportation Allowance',
            'description': 'Updated description'
        }
        response = self.client.put(f'/api/hr/benefit-type/{self.benefit_type.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Updated description')

    def test_delete_benefit_type(self):
        response = self.client.delete(f'/api/hr/benefit-type/{self.benefit_type.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BenefitType.objects.filter(id=self.benefit_type.id).exists())

    def test_get_nonexistent_benefit_type_returns_404(self):
        response = self.client.get('/api/hr/benefit-type/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_request_returns_401(self):
        self.client.credentials()
        response = self.client.get('/api/hr/benefit-type/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ─── EmployeeBenefit Tests ───────────────────────────────────────

class EmployeeBenefitTests(BaseHRTestCase):

    def setUp(self):
        super().setUp()
        self.benefit_type = BenefitType.objects.create(
            benefit_name='Transportation Allowance',
            description='Monthly transportation benefit'
        )
        self.employee_benefit = EmployeeBenefit.objects.create(
            employee=self.employee,
            benefit=self.benefit_type,
            amount=Decimal('2000.00'),
            effective_start_date=date(2024, 1, 1),
            effective_end_date=None
        )

    def test_get_all_employee_benefits(self):
        response = self.client.get('/api/hr/employee-benefit/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_single_employee_benefit(self):
        response = self.client.get(f'/api/hr/employee-benefit/{self.employee_benefit.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], '2000.00')

    def test_create_employee_benefit(self):
        new_benefit_type = BenefitType.objects.create(
            benefit_name='Meal Allowance',
            description='Daily meal'
        )
        data = {
            'employee': self.employee.id,
            'benefit': new_benefit_type.id,
            'amount': '1500.00',
            'effective_start_date': '2024-06-01',
        }
        response = self.client.post('/api/hr/employee-benefit/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['amount'], '1500.00')

    def test_create_employee_benefit_missing_fields_returns_400(self):
        response = self.client.post('/api/hr/employee-benefit/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_employee_benefit(self):
        data = {
            'employee': self.employee.id,
            'benefit': self.benefit_type.id,
            'amount': '2500.00',
            'effective_start_date': '2024-01-01',
        }
        response = self.client.put(
            f'/api/hr/employee-benefit/{self.employee_benefit.id}/', data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], '2500.00')

    def test_delete_employee_benefit(self):
        response = self.client.delete(
            f'/api/hr/employee-benefit/{self.employee_benefit.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            EmployeeBenefit.objects.filter(id=self.employee_benefit.id).exists()
        )

    def test_get_nonexistent_employee_benefit_returns_404(self):
        response = self.client.get('/api/hr/employee-benefit/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_employee_benefit_returns_404(self):
        data = {
            'employee': self.employee.id,
            'benefit': self.benefit_type.id,
            'amount': '2500.00',
            'effective_start_date': '2024-01-01',
        }
        response = self.client.put('/api/hr/employee-benefit/99999/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_request_returns_401(self):
        self.client.credentials()
        response = self.client.get('/api/hr/employee-benefit/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)