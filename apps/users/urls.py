from django.urls import path
from .views import UserCreateView
from . import views
from .views import (
    UserCreateView, UserDetailView, UserUpdateView, UserDeleteView, UserTransactionsView
)
urlpatterns = [
    path("create", UserCreateView.as_view(), name="user-create"),
    path("", views.list_users, name="list_users"),
    path("<int:pk>", UserDetailView.as_view(), name="user-detail"),  # GET by id
    path("update/<int:pk>", UserUpdateView.as_view(), name="user-update"),  # PATCH
    path("delete/<int:pk>", UserDeleteView.as_view(), name="user-delete"),  # DELETE
    path("<int:pk>/transactions", UserTransactionsView.as_view(), name="user-transactions"),
]
