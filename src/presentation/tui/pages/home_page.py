import questionary

from domain.services.alert_service import AlertService
from domain.services.budget_service import BudgetService
from domain.services.transaction_service import TransactionService


async def render(user_id: int, db):
    budget_service = BudgetService(db)
    alert_service = AlertService(db)
    transaction_service = TransactionService(db)

    print("\n=== 🏠 Home ===")

    budget = await budget_service.calculate_today_budget(user_id)
    if budget:
        print("\n💰 今日使える金額")
        print(f"  - 残り日数       : {budget['remaining_days']}日")
        print(f"  - 残り予算       : ¥{budget['remaining_budget']}")
        print(f"  - 1日あたり目安 : ¥{budget['per_day']}")

    alerts = await alert_service.get_alerts(user_id)
    if alerts:
        print("\n🔔 アラート")
        for msg in alerts:
            print(f" - {msg}")

    action = questionary.select(
        "\n--- Quick Actions ---", choices=["➕ Add income", "➖ Add expense", "⏭ Skip"]
    ).ask()

    if action == "➕ Add income":
        amount = int(questionary.text("金額を入力：").ask())
        category = questionary.text("カテゴリ：").ask()
        confirmed = questionary.confirm("確定済みですか？").ask()
        await transaction_service.add_income(user_id, amount, category, confirmed)
        print("✅ 収入を追加しました。")

    elif action == "➖ Add expense":
        amount = int(questionary.text("金額を入力：").ask())
        category = questionary.text("カテゴリ：").ask()
        await transaction_service.add_expense(user_id, amount, category)
        print("✅ 支出を追加しました。")
