from datetime import date, timedelta

from domain.services.setting_service import SettingService
from domain.services.transaction_service import TransactionService


class BudgetService:
    def __init__(self, db):
        self.setting_service = SettingService(db)
        self.transaction_service = TransactionService(db)

    async def calculate_today_budget(self, user_id: int):
        today = date.today()
        start_of_month = today.replace(day=1)
        next_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1)
        end_of_month = next_month - timedelta(days=1)
        remaining_days = (end_of_month - today).days + 1

        settings = await self.setting_service.get_settings(user_id)
        if not settings:
            print("Settings not found")
            return

        category = settings["category"]
        amount = settings["amount"]

        # sum of all expenses
        expenses = await self.transaction_service.get_expense_list(user_id)
        total_expense = sum(
            e["amount"] for e in expenses if start_of_month <= e["date"] <= today
        )

        remaining_budget = 0

        match category:
            case "budget":
                remaining_budget = amount - total_expense
            case "saving":
                incomes = await self.transaction_service.get_income_list(user_id)
                total_income = sum(
                    i["amount"]
                    for i in incomes
                    if start_of_month <= i["date"] <= today and i["confirmed"]
                )
                remaining_budget = total_income - total_expense - amount

        per_day = max(remaining_budget // remaining_days, 0)

        return {
            "remaining_budget": remaining_budget,
            "per_day": per_day,
            "remaining_days": remaining_days,
            "mode": category,
        }
