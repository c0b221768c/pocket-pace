import questionary

from domain.services.transaction_service import TransactionService


async def render(user_id: int, db):
    transaction_service = TransactionService(db)

    print("\n=== 🧾 History ===")

    incomes = await transaction_service.get_income_list(user_id)
    expenses = await transaction_service.get_expense_list(user_id)

    incomes.sort(key=lambda x: x["date"], reverse=True)
    expenses.sort(key=lambda x: x["date"], reverse=True)

    print("\n[ 収入一覧 ]")
    for i in incomes:
        status = "✅" if i["confirmed"] else "❌"
        print(
            f"ID: {i['id']} | {i['date']} | ¥{i['amount']} | {i['subcategory']} | {status}"
        )

    print("\n[ 支出一覧 ]")
    for e in expenses:
        print(f"ID: {e['id']} | {e['date']} | ¥{e['amount']} | {e['subcategory']}")

    action = questionary.select(
        "\n--- 操作 ---",
        choices=[
            "📝 Edit income",
            "📝 Edit expense",
            "❌ Delete income",
            "❌ Delete expense",
            "⏪ Back",
        ],
    ).ask()

    if action.startswith("📝 Edit income"):
        income_id = int(questionary.text("編集する収入ID：").ask())
        target = next((i for i in incomes if i["id"] == income_id), None)
        if not target:
            print("⚠️ 該当の収入が見つかりません。")
            return
        amount = (
            questionary.text(f"金額（{target['amount']}）:").ask() or target["amount"]
        )
        category = (
            questionary.text(f"カテゴリ（{target['subcategory']}）:").ask()
            or target["subcategory"]
        )
        date = (
            questionary.text(f"日付 YYYY-MM-DD（{target['date']}）:").ask()
            or target["date"]
        )
        confirmed = questionary.confirm("確定済みですか？").ask()
        await transaction_service.edit_income(
            income_id, int(amount), category, date, confirmed
        )

    elif action.startswith("📝 Edit expense"):
        expense_id = int(questionary.text("編集する支出ID：").ask())
        target = next((e for e in expenses if e["id"] == expense_id), None)
        if not target:
            print("⚠️ 該当の支出が見つかりません。")
            return
        amount = (
            questionary.text(f"金額（{target['amount']}）:").ask() or target["amount"]
        )
        category = (
            questionary.text(f"カテゴリ（{target['subcategory']}）:").ask()
            or target["subcategory"]
        )
        date = (
            questionary.text(f"日付 YYYY-MM-DD（{target['date']}）:").ask()
            or target["date"]
        )
        await transaction_service.edit_expense(expense_id, int(amount), category, date)

    elif action.startswith("❌ Delete income"):
        income_id = int(questionary.text("削除する収入ID：").ask())
        if questionary.confirm("本当に削除しますか？").ask():
            await transaction_service.delete_income(income_id)

    elif action.startswith("❌ Delete expense"):
        expense_id = int(questionary.text("削除する支出ID：").ask())
        if questionary.confirm("本当に削除しますか？").ask():
            await transaction_service.delete_expense(expense_id)
