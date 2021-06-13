from django.urls import path
from .views import AccountListView, TransactionViewSet, AccountViewSet

from rest_framework import routers


router = routers.DefaultRouter()
router.register('transactions', TransactionViewSet, basename='transactions')
router.register('accs', AccountViewSet, basename='accs')


urlpatterns = [
    path('accounts/', AccountListView.as_view()),
]

urlpatterns += router.urls
