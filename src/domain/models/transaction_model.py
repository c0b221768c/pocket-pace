class TransactionModel:
    def __init__(self, db):
        self.db = db

    # income
    async def add_income(self, user_id, amount, category, date, confirmed):
        await self.db.execute(
            "INSERT INTO income (user_id, amount, date, subcategory, confirmed) VALUES ($1, $2, $3, $4, $5)",
            user_id,
            amount,
            date,
            category,
            confirmed,
        )

    async def update_income(self, income_id, amount, category, date, confirmed):
        await self.db.execute(
            "UPDATE income SET amount = $1, date = $2, subcategory = $3, confirmed = $4 WHERE id = $5",
            amount,
            date,
            category,
            confirmed,
            income_id,
        )

    async def delete_income(self, income_id):
        await self.db.execute("DELETE FROM income WHERE id = $1", income_id)

    async def list_income(self, user_id):
        return await self.db.fetch(
            "SELECT * FROM income WHERE user_id = $1 ORDER BY date DESC", user_id
        )

    # expense
    async def add_expense(self, user_id, amount, category, date):
        await self.db.execute(
            "INSERT INTO expense (user_id, amount, date, subcategory) VALUES ($1, $2, $3, $4)",
            user_id,
            amount,
            date,
            category,
        )

    async def update_expenes(self, expense_id, amount, category, date):
        await self.db.execute(
            "UPDATE expense SET amount = $1, subcategory = $2, date = $3 WHERE id = $4",
            amount,
            category,
            date,
            expense_id,
        )

    async def delete_expense(self, expense_id):
        await self.db.execute("DELETE FROM expense WHERE id = $1", expense_id)

    async def list_expense(self, user_id):
        return await self.db.fetch(
            "SELECT * FROM expense WHERE user_id = $1 ORDER BY date DESC", user_id
        )
