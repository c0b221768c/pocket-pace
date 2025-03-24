from datetime import date

from domain.models.transaction_model import TransactionModel


class TransactionService:
    def __init__(self, db):
        self.model = TransactionModel(db)

    # income
    async def add_income(self, user_id, amount, category, confirmed=False, date_=None):
        await self.model.add_income(
            user_id, amount, category, date_ or date.today(), confirmed
        )

    async def edit_income(self, income_id, amount, category, date_, confirmed):
        await self.model.update_income(income_id, amount, category, date_, confirmed)

    async def delete_income(self, income_id):
        await self.model.delete_income(income_id)

    async def get_income_list(self, user_id):
        return await self.model.list_income(user_id)

    # expense
    async def add_expense(self, user_id, amount, category, date_=None):
        await self.model.add_expense(user_id, amount, category, date_ or date.today())

    async def edit_expense(self, expense_id, amount, category, date_):
        await self.model.update_expenes(expense_id, amount, category, date_)

    async def delete_expense(self, expense_id):
        await self.model.delete_expense(expense_id)

    async def get_expense_list(self, user_id):
        return await self.model.list_expense(user_id)
