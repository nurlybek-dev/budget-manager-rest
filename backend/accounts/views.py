# accounts/views.py
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.auth import views

from .forms import CustomSetPasswordForm, CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordChangeForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class LoginView(views.LoginView):
    form_class = CustomAuthenticationForm
    template_name='registration/login.html'

    def render_to_response(self, context, **response_kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('index'))
        return super().render_to_response(context, **response_kwargs)


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'


class SettingView(views.PasswordChangeView):
    form_class = CustomPasswordChangeForm
