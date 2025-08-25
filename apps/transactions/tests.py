from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.transactions.models import Transaction

User = get_user_model()

class TransactionTests(TestCase):
    def setUp(self):
        self.u1 = User.objects.create(email="a@a.com", balance=2000)
        self.u2 = User.objects.create(email="b@b.com", balance=1000)

    def test_create_transaction(self):
        tx = Transaction.objects.create(
            from_user=self.u1,
            to_user=self.u2,
            amount=500,
            category="food",
            description="Test transfer"
        )

        self.assertEqual(tx.amount, 500)
        self.assertEqual(tx.from_user, self.u1)
        self.assertEqual(tx.to_user, self.u2)
        self.assertEqual(tx.category, "food")
        self.assertTrue(tx.created_at is not None)

