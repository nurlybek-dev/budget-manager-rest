from main.models import Account, Transaction
from django.db.models import Sum, When, Count, Case
from django.db.models.functions.datetime import ExtractMonth, ExtractYear
from django.db.models import Sum, CharField, Value as V
from django.db.models.functions import Concat

def get_last_transactions(user, *args, **kwargs) -> dict:
    """Retrun last transactions with total amount for the day"""
    last_week = user.transactions.filter(*args, **kwargs).values('date').distinct().order_by('-date')
    
    data = []
    for day in last_week:
        transactions = user.transactions.filter(date=str(day['date']), *args, **kwargs).distinct()
        positive_transactions = transactions.filter(source__in=Account.objects.filter(user=user, type=Account.INCOME))
        negative_transactions = transactions.filter(destination__in=Account.objects.filter(user=user, type=Account.EXPENSE))

        total = (positive_transactions.aggregate(Sum('amount'))['amount__sum'] or 0) - (negative_transactions.aggregate(Sum('amount'))['amount__sum'] or 0)
        
        data.append({
            'day': day['date'],
            'transactions': transactions,
            'total': total
        })

    return data


def get_category_summary(user, category, month) -> dict:
    """Return accounts, actual and planned amount for the category"""
    accounts = user.accounts.filter(type=category)

    if category == Account.INCOME:
        category_actual = Transaction.objects.filter(date__month=month, source__in=accounts).aggregate(Sum('amount'))['amount__sum']
    elif category == Account.DEPOSIT:
        category_actual = accounts.aggregate(Sum('actual_amount'))['actual_amount__sum']
    elif category == Account.EXPENSE:
        category_actual = Transaction.objects.filter(date__month=month, destination__in=accounts).aggregate(Sum('amount'))['amount__sum']

    category_planned = accounts.aggregate(Sum('planned_amount'))['planned_amount__sum']
    expenses_summary = {
        'accounts': accounts,
        'actual': category_actual or 0,
        'planned': category_planned
    }

    return expenses_summary


def get_chart_data(account):
    income_query = When(source_id=0, then='amount')
    expense_query = When(destination_id=0, then='amount')
    if account.type == Account.INCOME:
        income_query = When(source_id=account.id, then='amount')
    elif account.type == Account.DEPOSIT:
        income_query = When(destination_id=account.id, then='amount')
        expense_query = When(source_id=account.id, then='amount')
    elif account.type == Account.EXPENSE:
        expense_query = When(destination_id=account.id, then='amount')
    
    result = Transaction.objects.values('date__month').annotate(
        count=Count('date__month'),
        d=Concat(ExtractYear('date'), V('-'), ExtractMonth('date'), output_field=CharField()),
        income=Sum(Case(income_query, default=0, output_field=CharField())),
        expense=Sum(Case(expense_query, default=0, output_field=CharField())),
    ).values('d', 'income', 'expense')

    return list(result)
