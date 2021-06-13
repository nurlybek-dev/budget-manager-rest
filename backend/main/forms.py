from django import forms
from django.contrib.auth import get_user
from django.db.models.query_utils import Q
from django.forms import ModelForm, widgets
from .models import Account, Transaction
from django.utils.translation import gettext_lazy as _


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'actual_amount', 'planned_amount']


class IncomeAccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'planned_amount']
        widgets = {
            'planned_amount': widgets.TextInput(attrs={'placeholder': _('Сколько планируете получать в месяц?')})
        }

    def save(self, user, commit=False):
        instance = super().save(commit=commit)

        instance.user = user
        instance.type = Account.INCOME
        instance.actual_amount = 0

        if not instance.planned_amount:
            instance.planned_amount = 0

        instance.save()
        return instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': _('Источник дохода')})

class DepositAccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'actual_amount']
        widgets = {
            'actual_amount': widgets.TextInput(attrs={'placeholder': _('Сколько там сейчас денег?')})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': _('Где вы храните деньги?')})

    def save(self, user, commit=False):
        instance = super().save(commit=commit)

        instance.user = user
        instance.type = Account.DEPOSIT
        instance.planned_amount = 0

        if not instance.actual_amount:
            instance.actual_amount = 0

        instance.save()
        return instance

class ExpenseAccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'planned_amount']
        widgets = {
            'planned_amount': widgets.TextInput(attrs={'placeholder': _('Сколько планируете тратить в месяц?')})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': _('На что будите тратить?')})


    def save(self, user, commit=False):
        instance = super().save(commit=commit)

        instance.user = user
        instance.type = Account.EXPENSE
        instance.actual_amount = 0
        
        if not instance.planned_amount:
            instance.planned_amount = 0

        instance.save()
        return instance


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['source', 'destination', 'amount', 'tags', 'comment', 'date']


    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['amount'].widget.attrs.update({'placeholder': _("1000")})
        self.fields['tags'].widget.attrs.update({'placeholder': _("Tag")})
        self.fields['comment'].widget.attrs.update({'placeholder': _("Comment")})
        self.fields['date'].widget = forms.DateInput(attrs={'type':'date'})

        sources = user.accounts.filter(Q(type=Account.INCOME) | Q(type=Account.DEPOSIT))
        destinations = user.accounts.filter(Q(type=Account.DEPOSIT) | Q(type=Account.EXPENSE))
        cource_choices = []
        for source in sources:
            cource_choices.append((source.id, source.name))

        destination_choices = []
        for destination in destinations:
            destination_choices.append((destination.id, destination.name))
            
        self.fields['source'].choices = cource_choices
        self.fields['destination'].choices = destination_choices
