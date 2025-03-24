from datetime import date


class SettingModel:
    def __init__(self, db):
        self.db = db

    async def get_by_user_id(self, user_id: int):
        rows = await self.db.fetch(
            "SELECT * FROM financial_settings WHERE user_id = $1",
            user_id,
        )
        return rows[0] if rows else None

    async def create(
        self,
        user_id: int,
        category: str,
        setting_type: str,
        amount: int,
        salary_days=None,
    ):
        await self.db.execute(
            """
            INSERT INTO financial_settings (user_id, category, setting_type, amount, salary_days)
            VALUES ($1, $2, $3, $4, $5)
            """,
            user_id,
            category,
            setting_type,
            amount,
            salary_days or [],
        )

    async def update(
        self,
        user_id: int,
        category: str,
        setting_type: str,
        amount: int,
        salary_days=None,
    ):
        await self.db.execute(
            """
            UPDATE financial_settings
            SET category = $1, setting_type = $2, amount = $3, salary_days = $4
            WHERE user_id = $5
            """,
            category,
            setting_type,
            amount,
            salary_days or [],
            user_id,
        )

    async def set_alert_flags(
        self, user_id: int, monthly_shown=None, salary_shown=None
    ):
        updates = []
        values = []

        if monthly_shown is not None:
            updates.append("monthly_input_alert_shown = $" + str(len(values) + 1))
            values.append(monthly_shown)
        if salary_shown is not None:
            updates.append("salary_alert_shown = $" + str(len(values) + 1))
            values.append(salary_shown)

        if updates:
            query = f"""
            UPDATE financial_settings
            SET {", ".join(updates)}
            WHERE user_id = ${len(values) + 1}
            """
            values.append(user_id)
            await self.db.execute(query, *values)

    async def reset_alert_flags_if_new_month(self, user_id: int):
        today = date.today()
        # query = """
        #     UPDATE financial_settings
        #     SET monthly_input_alert_shown = FALSE,
        #         salary_alert_shown = FALSE
        #     WHERE user_id = $1
        #         AND (
        #             EXTRACT(MONTH FROM CURRENT_DATE) != EXTRACT(MONTH FROM latest_alert_reset)
        #             OR last_alert_reset IS NULL
        #             );

        #     UPDATE financial_settings
        #     SET last_alert_reset = $2
        #     WHERE user_id = $1;
        # """
        # await self.db.execute(query, user_id, today)
        await self.db.execute(
            """
            UPDATE financial_settings
            SET monthly_input_alert_shown = FALSE,
                salary_alert_shown = FALSE
            WHERE user_id = $1
                AND (
                    EXTRACT(MONTH FROM CURRENT_DATE) != EXTRACT(MONTH FROM last_alert_reset)
                    OR last_alert_reset IS NULL
                    );
            """,
            user_id,
        )

        await self.db.execute(
            """UPDATE financial_settings
            SET last_alert_reset = $1
            WHERE user_id = $2""",
            today,
            user_id,
        )
