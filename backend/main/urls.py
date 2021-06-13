# accounts/urls.py
from django.urls import path, include

from .views import (
    add_transaction,
    delete_account,
    delete_transaction,
    get_accounts_by_source,
    index,
    add_income_account,
    add_deposit_account,
    add_expense_account,
    edit_account,
    edit_transaction,
    account_detail,
    chart_data
)


urlpatterns = [
    path('', index, name='index'),
    path('add-income/', add_income_account, name='add-income'),
    path('add-deposit/', add_deposit_account, name='add-deposit'),
    path('add-expense/', add_expense_account, name='add-expense'),
    path('edit-account/<int:pk>/', edit_account, name='edit-account'),
    path('delete-account/<int:pk>/', delete_account, name='delete-account'),

    path('add-transaction/', add_transaction, name='add-transaction'),
    path('delete-transaction/', delete_transaction, name='delete-transaction'),
    path('edit-transaction/<int:pk>/', edit_transaction, name='edit-transaction'),

    path('get-accounts-by-source/', get_accounts_by_source, name='get-destination-accounts'),

    path('<int:pk>/', account_detail, name='account-detail'),
    path('chart-data/<int:pk>/', chart_data, name='chart-data'),

    path('api/v1/', include('main.api.urls')),
]
