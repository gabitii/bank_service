from rest_framework import serializers
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import transaction as db_transaction
from .models import Transaction

User = get_user_model()

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "from_user", "to_user", "amount", "category", "description", "created_at"]
        read_only_fields = ["id", "created_at"]


class TransactionCreateSerializer(serializers.ModelSerializer):
    from_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    to_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Transaction
        fields = ["id", "from_user", "to_user", "amount", "category", "description", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_amount(self, value):
        if value <= Decimal("0"):
            raise serializers.ValidationError("Amount must be positive.")
        return value

    def validate(self, data):
        if data["from_user"].pk == data["to_user"].pk:
            raise serializers.ValidationError("from_user and to_user must be different.")
        return data

    def create(self, validated_data):
        amount = validated_data["amount"]
        from_user = validated_data["from_user"]
        to_user = validated_data["to_user"]

        with db_transaction.atomic():
            sender = User.objects.select_for_update().get(pk=from_user.pk)
            receiver = User.objects.select_for_update().get(pk=to_user.pk)

            if sender.balance < amount:
                raise serializers.ValidationError({"amount": "Insufficient funds."})

            sender.balance = sender.balance - amount
            receiver.balance = receiver.balance + amount
            sender.save()
            receiver.save()

            tx = Transaction.objects.create(**validated_data)
            return tx
