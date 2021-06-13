from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.db.models.aggregates import Sum
from django.utils import timezone

class Account(models.Model):
    INCOME = 1
    DEPOSIT = 2
    EXPENSE = 3
    TYPES = [
        (INCOME, 'Income'),
        (DEPOSIT, 'Deposit'),
        (EXPENSE, 'Expense'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='accounts')
    type = models.IntegerField(choices=TYPES)
    name = models.CharField(max_length=128)
    actual_amount = models.FloatField(blank=True)
    planned_amount = models.FloatField(blank=True)
    icon = models.CharField(max_length=255, blank=True, default="icon.png")

    def current_month_amount(self):
        if self.type is Account.DEPOSIT:
            return self.actual_amount
        
        current_month = timezone.now().month
        if self.type is Account.INCOME:
            return self.source_transactions \
                .filter(date__month=current_month) \
                .aggregate(Sum('amount'))['amount__sum'] or 0
    
        if self.type is Account.EXPENSE:
            return self.destination_transactions \
                .filter(date__month=current_month) \
                .aggregate(Sum('amount'))['amount__sum'] or 0

    def get_fill_percent(self):
        if self.planned_amount == 0:
            return 100
        
        return self.current_month_amount() * 100 / self.planned_amount

    def get_absolute_url(self):
        return f'/account/{self.id}'
    

    def __repr__(self) -> str:
        return f'<Account {self.name}>'

    def __str__(self) -> str:
        return '<Account %s/%s>' % (str(self.user), self.name)


class Transaction(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='transactions')
    source = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='source_transactions')
    destination = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='destination_transactions')
    amount = models.FloatField()
    tags = models.CharField(max_length=255, default='', blank=True)
    comment = models.CharField(max_length=255, default='', blank=True)
    date = models.DateField()

    def type(self):
        if self.source.type == Account.INCOME and self.destination.type == Account.DEPOSIT:
            return 'transaction_type_positive'
        elif self.source.type == Account.DEPOSIT and self.destination.type == Account.EXPENSE:
            return 'transaction_type_negative'
        else:
            return ''

    def __str__(self) -> str:
        return "<Transaction %s. %s -> %s>" % (str(self.user), self.source.name, self.destination.name)

    @transaction.atomic
    def delete(self, *args, **kwargs):
        if self.source.type == Account.DEPOSIT:
            self.source.actual_amount += self.amount
            self.source.save()
        if self.destination.type == Account.DEPOSIT:
            self.destination.actual_amount -= self.amount
            self.destination.save()
        return super().delete(*args, **kwargs)
