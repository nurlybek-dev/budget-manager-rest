from django.db.models.query_utils import Q

from django.http.response import JsonResponse
from django.core.paginator import Paginator
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db import transaction

from django.utils import timezone

from .models import Account, Transaction
from .forms import AccountForm, IncomeAccountForm, DepositAccountForm, ExpenseAccountForm, TransactionForm

from .services import get_category_summary, get_chart_data, get_last_transactions


@login_required
def index(request):
    today = timezone.now()

    incomes = get_category_summary(request.user, Account.INCOME, today.month)
    deposits = get_category_summary(request.user, Account.DEPOSIT, today.month)
    expenses = get_category_summary(request.user, Account.EXPENSE, today.month)
    
    transactions = get_last_transactions(request.user)
    paginator  = Paginator(transactions, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_count = paginator.num_pages

    income_form = IncomeAccountForm()
    deposit_form = DepositAccountForm()
    expense_form = ExpenseAccountForm()

    if request.is_ajax():
        return render(request, 'main/transaction_list.html', context={'page_obj': page_obj})

    context = {
        'today': today,
        'incomes': incomes,
        'deposits': deposits,
        'expenses': expenses,
        'income_form': income_form,
        'deposit_form': deposit_form,
        'expense_form': expense_form,
        'page_obj': page_obj,
        'page_count': page_count
    }
    return render(request, 'main/index.html', context=context)


@login_required
def account_detail(request, pk):
    today = timezone.now()
    account = get_object_or_404(Account, pk=pk, user=request.user)

    transactions = get_last_transactions(request.user, Q(source=account) | Q(destination=account))
    paginator  = Paginator(transactions, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    incomes = get_category_summary(request.user, Account.INCOME, today.month)
    deposits = get_category_summary(request.user, Account.DEPOSIT, today.month)
    expenses = get_category_summary(request.user, Account.EXPENSE, today.month)

    context = {
        'today': today,
        'account': account,
        'page_obj': page_obj,
        'incomes': incomes,
        'deposits': deposits,
        'expenses': expenses
    }

    return render(request, 'main/account_detail.html', context=context)


@login_required
def chart_data(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    data = get_chart_data(account)
    context = {
        'data': data
    }

    return JsonResponse(context)


@login_required 
def add_income_account(request):
    if request.method == 'POST':
        form = IncomeAccountForm(request.POST)
        if form.is_valid():
            form.save(request.user)
        else:
            print(form.errors)

    return redirect(reverse('index'))


@login_required
def add_deposit_account(request):
    if request.method == 'POST':
        form = DepositAccountForm(request.POST)
        if form.is_valid():
            form.save(request.user)
        else:
            print(form.errors)

    return redirect(reverse('index'))


@login_required
def add_expense_account(request):
    if request.method == 'POST':
        form = ExpenseAccountForm(request.POST)
        if form.is_valid():
            form.save(request.user)
        else:
            print(form.errors)

    return redirect(reverse('index'))


@login_required
def edit_account(request, pk):
    account = get_object_or_404(Account, pk=pk)

    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return redirect(reverse('index'))
    
    response_data = {
        'name': account.name,
        'actual_amount': account.actual_amount,
        'planned_amount': account.planned_amount,
    }

    return JsonResponse(response_data)


@login_required
def delete_account(request, pk):
    account = get_object_or_404(Account, pk=pk, user=request.user)
    account.delete()
    return redirect(reverse('index'))


@login_required
@transaction.atomic
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.user, request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()

            if transaction.source.type != Account.INCOME:
                transaction.source.actual_amount -= transaction.amount
                transaction.source.save()
            if transaction.destination.type != Account.EXPENSE:
                transaction.destination.actual_amount += transaction.amount
                transaction.destination.save()
        else:
            print(form.errors)


    return redirect(reverse('index'))


@login_required
@transaction.atomic
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        prev_amount = transaction.amount
        form = TransactionForm(request.user, request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save()

            if transaction.source.type != Account.INCOME:
                transaction.source.actual_amount -= transaction.amount + prev_amount
                transaction.source.save()
            if transaction.destination.type != Account.EXPENSE:
                transaction.destination.actual_amount += transaction.amount - prev_amount
                transaction.destination.save()
        else:
            print(form.errors)


    return redirect(reverse('index'))


@login_required
@transaction.atomic
def delete_transaction(request):
    if request.method == 'POST':
        transaction = get_object_or_404(Transaction, pk=request.POST.get('id'))

        if transaction.source.type == Account.DEPOSIT:
            transaction.source.actual_amount += transaction.amount
            transaction.source.save()
        if transaction.destination.type == Account.DEPOSIT:
            transaction.destination.actual_amount -= transaction.amount
            transaction.destination.save()

        transaction.delete()

    return redirect(reverse('index'))


@login_required
def get_accounts_by_source(request):
    source_id = request.GET.get('source')
    
    if source_id:
        source = get_object_or_404(Account, pk=source_id, user=request.user)
        accounts = request.user.accounts
        if source.type == Account.INCOME:
            accounts = accounts.filter(type=Account.DEPOSIT)
        elif source.type == Account.DEPOSIT:
            accounts = accounts.all().exclude(type=Account.INCOME).exclude(id=source_id)

        response_data = {
            'accounts': list(accounts.values('id', 'name'))
        }
    else:
        accounts = list(request.user.accounts.filter(type__in=[Account.INCOME, Account.DEPOSIT]).values('id', 'name'))
        response_data = {   
            'accounts': accounts
        }

    return JsonResponse(response_data)
