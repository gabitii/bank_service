from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.transactions.models import Transaction
from .utils import generate_report

class ReportSummaryView(APIView):
    def get(self, request):
        user_id = request.query_params.get("user_id")
        period = request.query_params.get("period", "last_30d")

        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        qs = Transaction.objects.filter(from_user_id=user_id) | Transaction.objects.filter(to_user_id=user_id)

        report_text = generate_report(qs, period, user_id)

        return Response({
            "user_id": user_id,
            "period": period,
            "report": report_text
        })
