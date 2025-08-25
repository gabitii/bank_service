import os
from django.conf import settings

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

client = None
if os.getenv("OPENAI_API_KEY"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_report(transactions, period: str, user_id):
    print("DBUG .env: ", os.getenv("OPENAI_API_KEY"))
    api_key= os.getenv("OPENAI_API_KEY")
    if OpenAI and api_key:
        context = "\n".join([
            f"{t.created_at.date()} | {t.from_user.name} -> {t.to_user.name} | {t.amount} | {t.category or 'N/A'}"
            for t in transactions
        ])

        prompt = f"""
        Ты финансовый аналитик. Составь короткий отчёт (3–5 пунктов) по транзакциям пользователя.
        Период: {period}.
        Транзакции:
        {context}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
        )

        return response.choices[0].message.content.strip()

    else:
        total_in = sum(t.amount for t in transactions if t.to_user_id == int(user_id))
        total_out = sum(t.amount for t in transactions if t.from_user_id == int(user_id))
        top_category = None
        if transactions:
            cats = {}
            for t in transactions:
                if t.category:
                    cats[t.category] = cats.get(t.category, 0) + float(t.amount)
            if cats:
                top_category = max(cats, key=cats.get)

        return (
            f"Мок-отчёт за {period}:\n"
            f"- Всего поступлений: {total_in}\n"
            f"- Всего расходов: {total_out}\n"
            f"- Топ категория: {top_category or 'нет данных'}"
        )
