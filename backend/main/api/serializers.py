from django.db import transaction
from main.models import Account, Transaction
from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'type', 'name', 'current_month_amount', 'actual_amount', 'planned_amount', 'get_fill_percent', 'get_absolute_url']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'source', 'destination', 'amount', 'tags', 'comment', 'date']

    @transaction.atomic
    def create(self, validated_data):
        instance = super().create(validated_data)

        if instance.source.type == Account.DEPOSIT:
            instance.source.actual_amount -= instance.amount
            instance.source.save()
        if instance.destination.type == Account.DEPOSIT:
            instance.destination.actual_amount += instance.amount
            instance.destination.save()
    
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        prev_amount = instance.amount
        prev_source = instance.source
        prev_destination = instance.destination
        new_instance = super().update(instance, validated_data)

        if new_instance.source == prev_source:
            if new_instance.source.type == Account.DEPOSIT:
                new_instance.source.actual_amount -= new_instance.amount - prev_amount
                new_instance.source.save()
        else:
            prev_source.actual_amount += prev_amount
            prev_source.save()
            new_instance.source.actual_amount -= new_instance.amount
            new_instance.source.save()

        if new_instance.destination == prev_destination:
            if new_instance.destination.type == Account.DEPOSIT:
                new_instance.destination.actual_amount += new_instance.amount - prev_amount
                new_instance.destination.save()
        else:
            prev_destination.actual_amount -= prev_amount
            prev_destination.save()
            new_instance.destination.actual_amount += new_instance.amount
            new_instance.destination.save()
        
        return new_instance



class TransactionListSerializer(serializers.ModelSerializer):
    source = AccountSerializer(read_only=True)
    destination = AccountSerializer(read_only=True)
    class Meta:
        model = Transaction
        fields = ['id', 'source', 'destination', 'amount', 'tags', 'comment', 'date']
