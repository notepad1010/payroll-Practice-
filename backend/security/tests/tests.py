from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from security.models.role import Role, Permission, RolePermission

User = get_user_model()


class BaseRoleTestCase(TestCase):
    """Base setup shared across all role/permission test cases."""

    def setUp(self):
        self.client = APIClient()

        # Staff user (admin)
        self.staff_user = User.objects.create_user(
            username='staff', password='pass123', is_staff=True
        )
        # Regular user (non-admin)
        self.regular_user = User.objects.create_user(
            username='regular', password='pass123', is_staff=False
        )

        # Sample role
        self.role = Role.objects.create(name='Manager')

        # Sample permission
        self.permission = Permission.objects.create(
            permission_key='can_view_reports', description='Can view reports'
        )

    def auth_as_staff(self):
        self.client.force_authenticate(user=self.staff_user)

    def auth_as_regular(self):
        self.client.force_authenticate(user=self.regular_user)

    def unauth(self):
        self.client.force_authenticate(user=None)


# ─────────────────────────────────────────────
# RoleListView  GET /roles/   POST /roles/
# ─────────────────────────────────────────────

class RoleListViewTests(BaseRoleTestCase):

    ENDPOINT = '/api/roles/'

    # ── GET ──────────────────────────────────

    def test_get_roles_authenticated_returns_200(self):
        self.auth_as_regular()
        response = self.client.get(self.ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_roles_returns_list(self):
        self.auth_as_regular()
        response = self.client.get(self.ENDPOINT)
        self.assertIsInstance(response.data, list)

    def test_get_roles_unauthenticated_returns_401(self):
        self.unauth()
        response = self.client.get(self.ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ── POST ─────────────────────────────────

    def test_post_role_as_staff_returns_201(self):
        self.auth_as_staff()
        response = self.client.post(self.ENDPOINT, {'name': 'Developer'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Developer')

    def test_post_role_as_regular_user_returns_403(self):
        self.auth_as_regular()
        response = self.client.post(self.ENDPOINT, {'name': 'Developer'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('error', response.data)

    def test_post_role_invalid_data_returns_400(self):
        self.auth_as_staff()
        # Sending empty payload — name is required
        response = self.client.post(self.ENDPOINT, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_role_unauthenticated_returns_401(self):
        self.unauth()
        response = self.client.post(self.ENDPOINT, {'name': 'Developer'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ─────────────────────────────────────────────
# RoleDetailView  GET/PUT/DELETE /roles/<pk>/
# ─────────────────────────────────────────────

class RoleDetailViewTests(BaseRoleTestCase):

    def endpoint(self, pk=None):
        pk = pk or self.role.pk
        return f'/api/roles/{pk}/'

    # ── GET ──────────────────────────────────

    def test_get_existing_role_returns_200(self):
        self.auth_as_regular()
        response = self.client.get(self.endpoint())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.role.name)

    def test_get_nonexistent_role_returns_404(self):
        self.auth_as_regular()
        response = self.client.get(self.endpoint(pk=99999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_get_role_unauthenticated_returns_401(self):
        self.unauth()
        response = self.client.get(self.endpoint())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ── PUT ──────────────────────────────────

    def test_put_role_as_staff_updates_successfully(self):
        self.auth_as_staff()
        response = self.client.put(self.endpoint(), {'name': 'Senior Manager'}, format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_202_ACCEPTED])
        self.role.refresh_from_db()
        self.assertEqual(self.role.name, 'Senior Manager')

    def test_put_role_as_regular_user_returns_403(self):
        self.auth_as_regular()
        response = self.client.put(self.endpoint(), {'name': 'Hacker'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_nonexistent_role_returns_404(self):
        self.auth_as_staff()
        response = self.client.put(self.endpoint(pk=99999), {'name': 'Ghost'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_invalid_data_returns_400(self):
        self.auth_as_staff()
        response = self.client.put(self.endpoint(), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ── DELETE ───────────────────────────────

    def test_delete_role_as_staff_returns_204(self):
        self.auth_as_staff()
        response = self.client.delete(self.endpoint())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Role.objects.filter(pk=self.role.pk).exists())

    def test_delete_role_as_regular_user_returns_403(self):
        self.auth_as_regular()
        response = self.client.delete(self.endpoint())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_nonexistent_role_returns_404(self):
        self.auth_as_staff()
        response = self.client.delete(self.endpoint(pk=99999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_role_assigned_to_user_returns_400(self):
        """Roles with active user assignments must be blocked from deletion."""
        self.auth_as_staff()
        # Simulate an existing user_role relation
        self.role.user_role.create(user=self.regular_user)
        response = self.client.delete(self.endpoint())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)


# ─────────────────────────────────────────────
# AssignPermissionToRoleView  POST /roles/<pk>/permissions/
# ─────────────────────────────────────────────

class AssignPermissionToRoleViewTests(BaseRoleTestCase):

    def endpoint(self, pk=None):
        pk = pk or self.role.pk
        return f'/api/roles/{pk}/permissions/'

    def test_assign_valid_permissions_returns_200(self):
        self.auth_as_staff()
        response = self.client.post(
            self.endpoint(),
            {'permission_ids': [self.permission.pk]},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            RolePermission.objects.filter(role=self.role, permission=self.permission).exists()
        )

    def test_assign_permissions_replaces_existing(self):
        """Re-assigning should wipe old permissions and set the new ones."""
        old_perm = Permission.objects.create(permission_key='old_perm', description='Old')
        RolePermission.objects.create(role=self.role, permission=old_perm)

        self.auth_as_staff()
        response = self.client.post(
            self.endpoint(),
            {'permission_ids': [self.permission.pk]},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            RolePermission.objects.filter(role=self.role, permission=old_perm).exists()
        )
        self.assertTrue(
            RolePermission.objects.filter(role=self.role, permission=self.permission).exists()
        )

    def test_assign_invalid_permission_id_returns_400(self):
        self.auth_as_staff()
        response = self.client.post(
            self.endpoint(),
            {'permission_ids': [99999]},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_assign_permissions_as_regular_user_returns_403(self):
        self.auth_as_regular()
        response = self.client.post(
            self.endpoint(),
            {'permission_ids': [self.permission.pk]},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_assign_permissions_nonexistent_role_returns_404(self):
        self.auth_as_staff()
        response = self.client.post(
            self.endpoint(pk=99999),
            {'permission_ids': [self.permission.pk]},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_assign_empty_permission_list_clears_all(self):
        """Passing an empty list should remove all permissions from the role."""
        RolePermission.objects.create(role=self.role, permission=self.permission)
        self.auth_as_staff()
        response = self.client.post(
            self.endpoint(),
            {'permission_ids': []},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(RolePermission.objects.filter(role=self.role).exists())


# ─────────────────────────────────────────────
# PermissionListView  GET/POST /permissions/
# ─────────────────────────────────────────────

class PermissionListViewTests(BaseRoleTestCase):

    ENDPOINT = '/api/permissions/'

    def test_get_permissions_authenticated_returns_200(self):
        self.auth_as_regular()
        response = self.client.get(self.ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_permissions_ordered_by_key(self):
        self.auth_as_staff()
        Permission.objects.create(permission_key='aaa_perm', description='First')
        Permission.objects.create(permission_key='zzz_perm', description='Last')
        response = self.client.get(self.ENDPOINT)
        keys = [p['permission_key'] for p in response.data]
        self.assertEqual(keys, sorted(keys))

    def test_get_permissions_unauthenticated_returns_401(self):
        self.unauth()
        response = self.client.get(self.ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_permission_as_staff_returns_201(self):
        self.auth_as_staff()
        response = self.client.post(
            self.ENDPOINT,
            {'permission_key': 'can_edit', 'description': 'Can edit'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_permission_as_regular_user_returns_403(self):
        self.auth_as_regular()
        response = self.client.post(
            self.ENDPOINT,
            {'permission_key': 'can_edit', 'description': 'Can edit'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_permission_invalid_data_returns_400(self):
        self.auth_as_staff()
        response = self.client.post(self.ENDPOINT, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────────
# PermissionDetailsView  GET/PUT/DELETE /permissions/<pk>/
# ─────────────────────────────────────────────

class PermissionDetailsViewTests(BaseRoleTestCase):

    def endpoint(self, pk=None):
        pk = pk or self.permission.pk
        return f'/api/permissions/{pk}/'

    # ── GET ──────────────────────────────────

    def test_get_existing_permission_returns_200(self):
        self.auth_as_regular()
        response = self.client.get(self.endpoint())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['permission_key'], self.permission.permission_key)

    def test_get_nonexistent_permission_returns_404(self):
        self.auth_as_regular()
        response = self.client.get(self.endpoint(pk=99999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_get_permission_unauthenticated_returns_401(self):
        self.unauth()
        response = self.client.get(self.endpoint())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ── PUT ──────────────────────────────────

    def test_put_permission_as_staff_updates_successfully(self):
        self.auth_as_staff()
        response = self.client.put(
            self.endpoint(),
            {'permission_key': 'can_delete', 'description': 'Updated'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.permission.refresh_from_db()
        self.assertEqual(self.permission.permission_key, 'can_delete')

    def test_put_permission_as_regular_user_returns_403(self):
        self.auth_as_regular()
        response = self.client.put(
            self.endpoint(),
            {'permission_key': 'evil', 'description': 'Nope'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_nonexistent_permission_returns_404(self):
        self.auth_as_staff()
        response = self.client.put(
            self.endpoint(pk=99999),
            {'permission_key': 'ghost', 'description': 'Ghost'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_invalid_data_returns_400(self):
        self.auth_as_staff()
        response = self.client.put(self.endpoint(), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ── DELETE ───────────────────────────────

    def test_delete_permission_as_staff_returns_204(self):
        self.auth_as_staff()
        response = self.client.delete(self.endpoint())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Permission.objects.filter(pk=self.permission.pk).exists())

    def test_delete_permission_as_regular_user_returns_403(self):
        self.auth_as_regular()
        response = self.client.delete(self.endpoint())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_nonexistent_permission_returns_404(self):
        self.auth_as_staff()
        response = self.client.delete(self.endpoint(pk=99999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)