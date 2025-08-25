from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers, generics
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .models import User
from .serializers import UserSerializer, UserCreateSerializer
from apps.transactions.serializers import TransactionSerializer
from apps.transactions.models import Transaction
import json

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

class UserRetrieveView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

class UserTransactionsView(generics.ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("id") or self.kwargs.get("pk") or self.kwargs.get("user_id")
        direction = self.request.query_params.get("direction")
        qs = Transaction.objects.filter(
            Q(from_user_id=user_id) | Q(to_user_id=user_id)
        )
        if direction == "in":
            qs = qs.filter(to_user_id=user_id)
        elif direction == "out":
            qs = qs.filter(from_user_id=user_id)
        return qs.order_by("-created_at")

@csrf_exempt
def create_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = User.objects.create(
            email=data["email"],
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            balance=data.get("balance", 0),
        )
        user.set_password(data["password"])
        user.save()
        return JsonResponse({"id": user.id, "email": user.email}, status=201)
    return JsonResponse({"error": "Method not allowed"}, status=405)


def list_users(request):
    if request.method == "GET":
        users = User.objects.all().values("id", "email", "first_name", "last_name", "balance")
        return JsonResponse(list(users), safe=False)
    return JsonResponse({"error": "Method not allowed"}, status=405)
