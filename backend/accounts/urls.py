# accounts/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView

from .views import SignUpView, LoginView, PasswordResetConfirmView, SettingView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('settings/', SettingView.as_view(), name='settings'),
]
