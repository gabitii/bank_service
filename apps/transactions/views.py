# apps/transactions/views.py
from rest_framework import generics
from .models import Transaction
from .serializers import TransactionSerializer, TransactionCreateSerializer
from django.db.models import Q

class TransactionListView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class TransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionCreateSerializer

class TransactionDetailView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

