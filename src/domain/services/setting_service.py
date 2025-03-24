from domain.models.setting_model import SettingModel


class SettingService:
    def __init__(self, db):
        self.setting_model = SettingModel(db)

    async def get_settings(self, user_id: int):
        return await self.setting_model.get_by_user_id(user_id)

    async def set_settings(
        self,
        user_id: int,
        category: str,
        setting_type: str,
        amount: int,
        salary_days=None,
    ):
        existing = await self.setting_model.get_by_user_id(user_id)

        if existing:
            await self.setting_model.update(
                user_id, category, setting_type, amount, salary_days
            )
        else:
            await self.setting_model.create(
                user_id, category, setting_type, amount, salary_days
            )

    async def mark_alert_as_shown(self, user_id: int, monthly=None, salary=None):
        await self.setting_model.set_alert_flags(
            user_id, monthly_shown=monthly, salary_shown=salary
        )

    async def reset_alert_flags_if_needed(self, user_id: int):
        await self.setting_model.reset_alert_flags_if_new_month(user_id)
