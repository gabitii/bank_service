from django.test import TestCase
from apps.transactions.models import Transaction
from apps.reports.utils import generate_report
from django.contrib.auth import get_user_model

User = get_user_model()

class ReportTests(TestCase):
    def test_generate_report_mock(self):
        u1 = User.objects.create(email="a@a.com", balance=2000)
        u2 = User.objects.create(email="b@b.com", balance=1000)

        Transaction.objects.create(from_user=u1, to_user=u2, amount=500, category="food")
        Transaction.objects.create(from_user=u2, to_user=u1, amount=300, category="gift")

        qs = Transaction.objects.filter(from_user=u1) | Transaction.objects.filter(to_user=u1)
        report = generate_report(qs, "last_7d", user_id=u1.id)

        self.assertTrue("поступлений" in report or "расходов" in report)
        self.assertNotIn(str(u1.email), report)