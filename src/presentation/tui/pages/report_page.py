from datetime import date, timedelta

from domain.services.transaction_service import TransactionService


def get_start_of_week(today):
    return today - timedelta(days=today.weekday())


async def render(user_id: int, db):
    transaction_service = TransactionService(db)
    today = date.today()
    start_of_week = get_start_of_week(today)
    start_of_month = today.replace(day=1)

    income_list = await transaction_service.get_income_list(user_id)
    expense_list = await transaction_service.get_expense_list(user_id)

    week_income = sum(
        i["amount"] for i in income_list if start_of_week <= i["date"] <= today
    )
    month_income = sum(
        i["amount"] for i in income_list if start_of_month <= i["date"] <= today
    )

    week_expense = sum(
        e["amount"] for e in expense_list if start_of_week <= e["date"] <= today
    )
    month_expense = sum(
        e["amount"] for e in expense_list if start_of_month <= e["date"] <= today
    )

    print("\n=== 📈 Report ===")
    print(
        f"\n[ 今週の収支 ]\n - 収入: ¥{week_income}\n - 支出: ¥{week_expense}\n - 収支: ¥{week_income - week_expense}"
    )
    print(
        f"\n[ 今月の収支 ]\n - 収入: ¥{month_income}\n - 支出: ¥{month_expense}\n - 収支: ¥{month_income - month_expense}"
    )

    print("\n[ カテゴリ別支出（今月） ]")
    category_totals = {}
    for e in expense_list:
        if start_of_month <= e["date"] <= today:
            cat = e["subcategory"]
            category_totals[cat] = category_totals.get(cat, 0) + e["amount"]

    for cat, total in sorted(category_totals.items(), key=lambda x: -x[1]):
        print(f" - {cat}: ¥{total}")
