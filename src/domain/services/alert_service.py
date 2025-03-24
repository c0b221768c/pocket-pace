from datetime import date

from domain.services.setting_service import SettingService
from domain.services.transaction_service import TransactionService


class AlertService:
    def __init__(self, db):
        self.setting_service = SettingService(db)
        self.transaction_service = TransactionService(db)

    async def get_alerts(self, user_id: int):
        alerts = []
        today = date.today()

        settings = await self.setting_service.get_settings(user_id)
        if not settings:
            return []

        category = settings.get("category")
        setting_type = settings.get("setting_type")
        salary_days = settings.get("salary_days") or []
        monthly_shown = settings.get("monthly_input_alert_shown", False)
        salary_shown = settings.get("salary_alert_shown", False)

        if setting_type == "variable" and not monthly_shown:
            if category == "budget":
                alerts.append("Please input your monthly budget")
            elif category == "saving":
                alerts.append("Please input your expected income")

        if category == "saving" and not salary_shown and today.day in salary_days:
            incomes = await self.transaction_service.get_income_list(user_id)
            has_unconfirmed_today = any(
                i["date"] == today and not i["confirmed"] for i in incomes
            )
            if has_unconfirmed_today:
                alerts.append(
                    "Is your salary credited today? Please confirm your income."
                )

        return alerts
