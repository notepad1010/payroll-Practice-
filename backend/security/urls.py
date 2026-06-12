from django.urls import path
from security.views.auth_views import LoginView,LogoutView,ChangePasswordView,PasswordResetRequestView,PasswordResetConfirmView

urlpatterns = [
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('change-password/',ChangePasswordView.as_view()),
    path('password-reset/',PasswordResetRequestView.as_view()),
    path('password-reset/confirm',PasswordResetConfirmView.as_view()),
]