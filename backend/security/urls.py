from django.urls import path
from security.views.auth_views import (LoginView,
                                       LogoutView,
                                       ChangePasswordView,
                                       PasswordResetRequestView,
                                       PasswordResetConfirmView)
from security.views.user_view import(AccountDetailsView,
                                     LockUnlockUserView,
                                     UserAccountlistView)
from security.views.role_views import(RoleListView,
                                      PermissionListView,
                                      RoleDetailView,
                                      PermissionDetailsView,
                                      AssignPermissionToRoleView
                                      )


urlpatterns = [
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('change-password/',ChangePasswordView.as_view()),
    path('password-reset/',PasswordResetRequestView.as_view()),
    path('password-reset/confirm',PasswordResetConfirmView.as_view()),
    path('user/',UserAccountlistView.as_view()),
    path('user/<int:pk>/',AccountDetailsView.as_view()),
    path('user/<int:pk>/<str:action>/',LockUnlockUserView.as_view()),
    path('roles/',RoleListView.as_view()),
    path('roles/<int:pk>/',RoleDetailView.as_view()),
    path('roles/<int:pk>/assign-permission/',AssignPermissionToRoleView.as_view()),
    path('permission/',PermissionListView.as_view()),
    path('permission/<int:pk>/',PermissionDetailsView.as_view()),
]