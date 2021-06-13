from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm, PasswordChangeForm, SetPasswordForm
)
from django import forms

from django.utils.translation import gettext_lazy as _

from .models import CustomUser
from main.models import Account


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':_('Email')}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'placeholder': _('Password')})
        self.fields['password2'].widget.attrs.update({'placeholder': _('Password confirmation')})

    def save(self, commit=True):
        instance = super().save(commit=commit)            
        INCOMES = ['Доход']
        DEPOSITS = ['Кошелек', 'Карта']
        EXPENSES = ['Продукты', 'Еда вне дома', 'Транспорт', 'Покупки', 'Услуги', 'Дом', 'Аптека', 'Развлечения', 'Разное']

        for income in INCOMES:
            account = Account(type=Account.INCOME, name=income, actual_amount=0, planned_amount=0, user=instance)
            account.save()
        
        for deposit in DEPOSITS:
            account = Account(type=Account.DEPOSIT, name=deposit, actual_amount=0, planned_amount=0, user=instance)
            account.save()
        
        for expense in EXPENSES:
            account = Account(type=Account.EXPENSE, name=expense, actual_amount=0, planned_amount=0, user=instance)
            account.save()
        
        return instance

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', )


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('email', )


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':_('Email')}))

    def __init__(self, request, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.fields['password'].widget.attrs.update({'placeholder': _('Password')})


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'placeholder': _('New password')})
        self.fields['new_password2'].widget.attrs.update({'placeholder': _('New password confirmation')})


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'placeholder': _('Old password')})
        self.fields['new_password1'].widget.attrs.update({'placeholder': _('New password')})
        self.fields['new_password2'].widget.attrs.update({'placeholder': _('New password confirmation')})