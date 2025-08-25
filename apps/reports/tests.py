from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.transactions.models import Transaction
from apps.reports.utils import generate_report

User = get_user_model()

class ReportTests(TestCase):
    def setUp(self):
        self.u1 = User.objects.create(email="a@a.com", balance=2000)
        self.u2 = User.objects.create(email="b@b.com", balance=1000)

        Transaction.objects.create(from_user=self.u1, to_user=self.u2, amount=500, category="food")
        Transaction.objects.create(from_user=self.u2, to_user=self.u1, amount=300, category="gift")

    def test_generate_report_for_user(self):
        qs = Transaction.objects.filter(from_user=self.u1) | Transaction.objects.filter(to_user=self.u1)
        report = generate_report(qs, "last_7d", user_id=self.u1.id)

        self.assertIn("поступлений", report)
        self.assertNotIn(self.u1.email, report)