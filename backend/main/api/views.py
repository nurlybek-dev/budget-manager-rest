from django.core.paginator import Paginator
from django.http.response import Http404

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from main.api.serializers import AccountSerializer, TransactionListSerializer, TransactionSerializer
from main.models import Transaction, Account
from main.api.permissions import IsOwner


class AccountListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        accounts = request.user.accounts.all()
        accounts_serializer = AccountSerializer(accounts, many=True)
        return Response(accounts_serializer.data)


class AccountViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self, pk):
        try:
            return Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            raise Http404

    def list(self, request):
        accounts = Account.objects.filter(user=request.user)
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        account = self.get_object(pk)
        serializer = AccountSerializer(account)
        return Response(serializer.data)

    def update(self, request, pk):
        account = self.get_object(pk)
        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        account = self.get_object(pk)
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self, pk):
        try:
            return Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            raise Http404

    def list(self, request):
        last_week = request.user.transactions.values('date').distinct().order_by('-date')
        paginator = Paginator(last_week, 7)
        page = request.GET.get('page')
        days = paginator.get_page(page).object_list

        transactions = request.user.transactions.filter(date__in=days).order_by('-date')
        transactions_serializers = TransactionListSerializer(transactions, many=True)

        return Response({'count': paginator.num_pages, 'results': transactions_serializers.data})
    
    def create(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(user=request.user)
            serializer = TransactionListSerializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(instance=transaction)
        return Response(serializer.data)

    def update(self, request, pk=None):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def partial_update(self, request, pk=None):
    #     pass

    def destroy(self, request, pk=None):
        transaction = self.get_object(pk)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
