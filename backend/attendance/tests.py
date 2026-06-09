from rest_framework.test import APITestCase
from rest_framework import status
from security.models import UserAccount
from attendance.models import Attendance, LeaveType, LeaveStatus
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

class AttendanceTests(BaseTestCase):

    def test_get_all_attendance(self):
        response = self.client.get('/api/attendance/attendance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_attendance(self):
        data = {
            'employee': self.employee.id,
            'work_date': '2024-06-01',
            'time_in': '08:00:00',
            'time_out': '17:00:00',
            'overtime_hours': 0,
            'attendance_status': 'PRESENT'
        }
        response = self.client.post(
            '/api/attendance/attendance/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_nonexistent_attendance(self):
        response = self.client.get('/api/attendance/attendance/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class LeaveTypeTests(BaseTestCase):

    def test_get_all_leave_types(self):
        response = self.client.get('/api/attendance/leave-type/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_leave_type(self):
        data = {
            'leave_name': 'Vacation Leave',
            'default_credits': 15,
            'is_paid': True,
            'is_active': True
        }
        response = self.client.post(
            '/api/attendance/leave-type/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['leave_name'], 'Vacation Leave')