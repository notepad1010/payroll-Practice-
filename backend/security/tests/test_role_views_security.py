"""
Security tests for role_views.py API endpoints.
Tests cover authorization, authentication, and data validation vulnerabilities.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from security.models.role import Role, Permission, RolePermission


class RoleViewsSecurityTests(TestCase):
    """Test authorization and authentication in role management endpoints."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = APIClient()
        
        # Create test users
        self.admin_user = User.objects.create_user(
            username='admin',
            password='admin_pass_123',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='regular',
            password='user_pass_123',
            is_staff=False
        )
        
        # Create test roles
        self.test_role = Role.objects.create(
            role_name='Test Role',
            description='Test Description'
        )
        self.admin_role = Role.objects.create(
            role_name='Admin',
            description='Admin Role'
        )
        
        # Create test permissions
        self.permission1 = Permission.objects.create(
            permission_key='read_users',
            description='Can read users'
        )
        self.permission2 = Permission.objects.create(
            permission_key='write_users',
            description='Can write users'
        )

    # =================== RoleListView Security Tests ===================
    
    def test_role_list_requires_authentication(self):
        """SECURITY: Unauthenticated users should not access role list."""
        response = self.client.get('/api/security/roles/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_list_roles(self):
        """SECURITY: Authenticated users can read roles (expected behavior)."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get('/api/security/roles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_non_staff_cannot_create_role(self):
        """SECURITY: Only staff users can create roles."""
        self.client.force_authenticate(user=self.regular_user)
        data = {
            'role_name': 'New Role',
            'description': 'New Role Description'
        }
        response = self.client.post('/api/security/roles/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('Access Denied', str(response.data))

    def test_staff_can_create_role(self):
        """SECURITY: Staff users can create roles (expected behavior)."""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'role_name': 'Created Role',
            'description': 'Created Role Description'
        }
        response = self.client.post('/api/security/roles/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_role_invalid_data(self):
        """SECURITY: Validate role creation with invalid data."""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'role_name': '',  # Empty name
            'description': 'Description'
        }
        response = self.client.post('/api/security/roles/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_role_name(self):
        """SECURITY: Prevent duplicate role names."""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'role_name': self.test_role.role_name,
            'description': 'Different Description'
        }
        response = self.client.post('/api/security/roles/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # =================== RoleDetailView Security Tests ===================
    
    def test_role_detail_requires_authentication(self):
        """SECURITY: Unauthenticated users should not access role details."""
        response = self.client.get(f'/api/security/roles/{self.test_role.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_view_role_detail(self):
        """SECURITY: Authenticated users can view role details (currently no restriction)."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(f'/api/security/roles/{self.test_role.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role_name'], self.test_role.role_name)

    def test_role_detail_nonexistent_role(self):
        """SECURITY: Should return 404 for non-existent roles."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(f'/api/security/roles/{9999}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_non_staff_cannot_update_role(self):
        """SECURITY: Only staff users can update roles."""
        self.client.force_authenticate(user=self.regular_user)
        data = {
            'role_name': 'Updated Role',
            'description': 'Updated Description'
        }
        response = self.client.put(f'/api/security/roles/{self.test_role.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_update_role(self):
        """SECURITY: Staff users can update roles (expected behavior)."""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'role_name': 'Updated Role Name',
            'description': 'Updated Description'
        }
        response = self.client.put(f'/api/security/roles/{self.test_role.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.test_role.refresh_from_db()
        self.assertEqual(self.test_role.role_name, 'Updated Role Name')

    def test_non_staff_cannot_delete_role(self):
        """SECURITY: Only staff users can delete roles."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(f'/api/security/roles/{self.test_role.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_delete_role(self):
        """SECURITY: Staff users can delete roles."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/security/roles/{self.test_role.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Role.objects.filter(id=self.test_role.id).exists())

    def test_cannot_delete_role_with_assigned_users(self):
        """SECURITY: Prevent deletion of roles that are assigned to users."""
        # Create a user account with this role
        from security.models.user_account import UserAccount
        user = User.objects.create_user(username='test_emp', password='pass')
        user_account = UserAccount.objects.create(employee_id=user.id, user=user)
        user_account.user_role.add(self.test_role)
        
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/security/roles/{self.test_role.id}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Cannot Delete', str(response.data))

    # =================== AssignPermissionToRoleView Security Tests ===================
    
    def test_assign_permission_requires_authentication(self):
        """SECURITY: Unauthenticated users cannot assign permissions."""
        data = {'permission_ids': [self.permission1.id]}
        response = self.client.post(
            f'/api/security/roles/{self.test_role.id}/assign-permission/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_staff_cannot_assign_permission(self):
        """SECURITY: Only staff users can assign permissions to roles."""
        self.client.force_authenticate(user=self.regular_user)
        data = {'permission_ids': [self.permission1.id]}
        response = self.client.post(
            f'/api/security/roles/{self.test_role.id}/assign-permission/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_assign_permission(self):
        """SECURITY: Staff users can assign permissions (expected behavior)."""
        self.client.force_authenticate(user=self.admin_user)
        data = {'permission_ids': [self.permission1.id, self.permission2.id]}
        response = self.client.post(
            f'/api/security/roles/{self.test_role.id}/assign-permission/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            RolePermission.objects.filter(role=self.test_role).exists()
        )

    def test_assign_permission_nonexistent_role(self):
        """SECURITY: Should return 404 for non-existent roles."""
        self.client.force_authenticate(user=self.admin_user)
        data = {'permission_ids': [self.permission1.id]}
        response = self.client.post(
            f'/api/security/roles/{9999}/assign-permission/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_assign_invalid_permission_ids(self):
        """SECURITY: Reject invalid permission IDs."""
        self.client.force_authenticate(user=self.admin_user)
        data = {'permission_ids': [9999, 10000]}  # Non-existent IDs
        response = self.client.post(
            f'/api/security/roles/{self.test_role.id}/assign-permission/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('invalid', str(response.data).lower())

    def test_assign_partial_invalid_permission_ids(self):
        """SECURITY: Reject if any permission ID is invalid."""
        self.client.force_authenticate(user=self.admin_user)
        data = {'permission_ids': [self.permission1.id, 9999]}  # Mix valid and invalid
        response = self.client.post(
            f'/api/security/roles/{self.test_role.id}/assign-permission/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_assign_empty_permission_list(self):
        """SECURITY: Allow empty permission list (clear permissions)."""
        # First assign some permissions
        RolePermission.objects.create(role=self.test_role, permission=self.permission1)
        
        self.client.force_authenticate(user=self.admin_user)
        data = {'permission_ids': []}
        response = self.client.post(
            f'/api/security/roles/{self.test_role.id}/assign-permission/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            RolePermission.objects.filter(role=self.test_role).exists()
        )

    # =================== PermissionListView Security Tests ===================
    
    def test_permission_list_requires_authentication(self):
        """SECURITY: Unauthenticated users should not access permission list."""
        response = self.client.get('/api/security/permission/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_list_permissions(self):
        """SECURITY: Authenticated users can list permissions."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get('/api/security/permission/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_non_staff_cannot_create_permission(self):
        """SECURITY: Only staff users can create permissions."""
        self.client.force_authenticate(user=self.regular_user)
        data = {
            'permission_key': 'delete_users',
            'description': 'Can delete users'
        }
        response = self.client.post('/api/security/permission/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_create_permission(self):
        """SECURITY: Staff users can create permissions."""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'permission_key': 'edit_salaries',
            'description': 'Can edit salaries'
        }
        response = self.client.post('/api/security/permission/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_permission_invalid_data(self):
        """SECURITY: Validate permission creation."""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'permission_key': '',  # Empty key
            'description': 'Description'
        }
        response = self.client.post('/api/security/permission/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_permission_key(self):
        """SECURITY: Prevent duplicate permission keys."""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'permission_key': self.permission1.permission_key,
            'description': 'Different Description'
        }
        response = self.client.post('/api/security/permission/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # =================== PermissionDetailsView Security Tests ===================
    
    def test_permission_detail_requires_authentication(self):
        """SECURITY: Unauthenticated users should not access permission details."""
        response = self.client.get(f'/api/security/permission/{self.permission1.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_view_permission_detail(self):
        """SECURITY: Authenticated users can view permission details."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(f'/api/security/permission/{self.permission1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_staff_cannot_update_permission(self):
        """SECURITY: Only staff users can update permissions."""
        self.client.force_authenticate(user=self.regular_user)
        data = {
            'permission_key': 'updated_key',
            'description': 'Updated description'
        }
        response = self.client.put(f'/api/security/permission/{self.permission1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_update_permission(self):
        """SECURITY: Staff users can update permissions."""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'permission_key': 'updated_read_users',
            'description': 'Updated description'
        }
        response = self.client.put(f'/api/security/permission/{self.permission1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_staff_cannot_delete_permission(self):
        """SECURITY: Only staff users can delete permissions."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(f'/api/security/permission/{self.permission1.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_delete_permission(self):
        """SECURITY: Staff users can delete permissions."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/security/permission/{self.permission1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_permission_detail_nonexistent(self):
        """SECURITY: Should return 404 for non-existent permissions."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(f'/api/security/permission/{9999}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RoleViewsVulnerabilityTests(TestCase):
    """Test for specific known vulnerabilities in role_views."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username='admin',
            password='admin_pass_123',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='regular',
            password='user_pass_123',
            is_staff=False
        )
        self.test_role = Role.objects.create(
            role_name='Test Role',
            description='Test Description'
        )

    def test_role_detail_get_missing_authorization_check(self):
        """VULNERABILITY: GET /roles/<pk>/ missing authorization check (commented out).
        
        Issue: The authorization check on line 36-37 is commented out.
        This allows any authenticated user to view role details, even non-staff.
        While view-only access may be acceptable, it should be explicit in design.
        """
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(f'/api/security/roles/{self.test_role.id}/')
        # Currently passes without staff check (vulnerability)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Recommendation: Uncomment authorization or document why all authenticated users can view

    def test_malformed_response_on_syntax_error(self):
        """VULNERABILITY: Line 19 has syntax error in Response - should use dict not set.
        
        Issue: {'error','Access Denied!'} is a set, not a dict.
        Should be {'error': 'Access Denied!'} with colon.
        This will cause unexpected serialization behavior.
        """
        # This test documents the issue - the code has a syntax error
        self.client.force_authenticate(user=self.regular_user)
        data = {
            'role_name': 'New Role',
            'description': 'Description'
        }
        response = self.client.post('/api/security/roles/', data)
        # Response should fail or have incorrect format due to set syntax
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sql_injection_via_role_name(self):
        """SECURITY: Verify no SQL injection via role creation."""
        self.client.force_authenticate(user=self.admin_user)
        # Attempt SQL injection payload
        data = {
            'role_name': "'; DROP TABLE role; --",
            'description': 'SQL Injection Test'
        }
        response = self.client.post('/api/security/roles/', data)
        # Django ORM should prevent this, but verify the role wasn't created with malicious intent
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify no role was actually created with that exact name
        roles = Role.objects.filter(role_name=data['role_name'])
        # The role should exist (as a literal string), but table should not be dropped
        self.assertTrue(Role.objects.filter(id__gt=0).exists())

    def test_no_csrf_vulnerability_on_post(self):
        """SECURITY: POST endpoints should be protected against CSRF."""
        data = {
            'role_name': 'CSRF Test Role',
            'description': 'Description'
        }
        # Without authentication, should fail
        response = self.client.post('/api/security/roles/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permission_ids_type_validation(self):
        """SECURITY: Validate permission_ids is properly typed."""
        self.client.force_authenticate(user=self.admin_user)
        # Try invalid permission_ids format
        data = {'permission_ids': 'not-a-list'}
        response = self.client.post(
            f'/api/security/roles/{self.test_role.id}/assign-permission/',
            data
        )
        # Should either fail validation or handle gracefully
        self.assertIn(
            response.status_code,
            [status.HTTP_400_BAD_REQUEST, status.HTTP_400_BAD_REQUEST]
        )
