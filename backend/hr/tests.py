from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from security.models import UserAccount
from hr.models import Department, Position, Employee

class BaseTestCase(APITestCase):
    """Base test case with authentication setup"""

    def setUp(self):
        # Create test user
        self.user = UserAccount.objects.create_superuser(
            username='testuser',
            password='Test@1234',
            email='test@payroll.com',
            company_email='test@payroll.com'
        )

        # Get JWT token
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'Test@1234'
        })
        self.token = response.data['access']

        # Set auth header
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )

        # Create test data
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

class DepartmentTests(BaseTestCase):

    def test_get_all_departments(self):
        """GET /api/hr/departments/ returns list"""
        response = self.client.get('/api/hr/departments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_single_department(self):
        """GET /api/hr/departments/<pk>/ returns single dept"""
        response = self.client.get(
            f'/api/hr/departments/{self.department.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['department_name'],
            'Information Technology'
        )

    def test_create_department(self):
        """POST /api/hr/departments/ creates new dept"""
        data = {
            'department_code': 'HR',
            'department_name': 'Human Resources',
            'is_active': True
        }
        response = self.client.post('/api/hr/departments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['department_name'], 'Human Resources')

    def test_update_department(self):
        """PUT /api/hr/departments/<pk>/ updates dept"""
        data = {
            'department_code': 'IT',
            'department_name': 'IT Department Updated',
            'is_active': True
        }
        response = self.client.put(
            f'/api/hr/departments/{self.department.id}/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['department_name'],
            'IT Department Updated'
        )

    def test_delete_department(self):
        """DELETE /api/hr/departments/<pk>/ deletes dept"""
        response = self.client.delete(
            f'/api/hr/departments/{self.department.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_nonexistent_department(self):
        """GET /api/hr/departments/999/ returns 404"""
        response = self.client.get('/api/hr/departments/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_request(self):
        """Request without token returns 401"""
        self.client.credentials()  # remove token
        response = self.client.get('/api/hr/departments/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ─── Position Tests ───────────────────────────────────────

class PositionTests(BaseTestCase):

    def test_get_all_positions(self):
        """GET /api/hr/positions/ returns list"""
        response = self.client.get('/api/hr/positions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_single_position(self):
        """GET /api/hr/positions/<pk>/ returns single position"""
        response = self.client.get(
            f'/api/hr/positions/{self.position.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['position_name'],
            'Software Developer'
        )

    def test_create_position(self):
        """POST /api/hr/positions/ creates new position"""
        data = {
            'position_name': 'Project Manager',
            'department': self.department.id,
            'is_active': True
        }
        response = self.client.post('/api/hr/positions/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['position_name'], 'Project Manager')

    def test_update_position(self):
        """PUT /api/hr/positions/<pk>/ updates position"""
        data = {
            'position_name': 'Senior Developer',
            'department': self.department.id,
            'is_active': True
        }
        response = self.client.put(
            f'/api/hr/positions/{self.position.id}/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_position(self):
        """DELETE /api/hr/positions/<pk>/ deactivates position"""
        response = self.client.delete(
            f'/api/hr/positions/{self.position.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_nonexistent_position(self):
        """GET /api/hr/positions/999/ returns 404"""
        response = self.client.get('/api/hr/positions/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# ─── Employee Tests ───────────────────────────────────────

class EmployeeTests(BaseTestCase):

    def test_get_all_employees(self):
        """GET /api/hr/employees/ returns list"""
        response = self.client.get('/api/hr/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_single_employee(self):
        """GET /api/hr/employees/<pk>/ returns single employee"""
        response = self.client.get(
            f'/api/hr/employees/{self.employee.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')

    def test_create_employee(self):
        """POST /api/hr/employees/ creates new employee"""
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

    def test_update_employee(self):
        """PUT /api/hr/employees/<pk>/ updates employee"""
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
        response = self.client.put(
            f'/api/hr/employees/{self.employee.id}/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deactivate_employee(self):
        """DELETE /api/hr/employees/<pk>/ deactivates employee"""
        response = self.client.delete(
            f'/api/hr/employees/{self.employee.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check employee is deactivated not deleted
        self.employee.refresh_from_db()
        self.assertFalse(self.employee.is_active)

    def test_get_nonexistent_employee(self):
        """GET /api/hr/employees/999/ returns 404"""
        response = self.client.get('/api/hr/employees/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)