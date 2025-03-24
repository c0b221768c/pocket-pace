import questionary

from domain.services.auth_service import AuthService
from domain.services.setting_service import SettingService


async def render(user_id: int, db):
    auth = AuthService(db)
    setting_service = SettingService(db)

    print("\n=== ⚙️ Settings ===")

    choice = questionary.select(
        "変更項目を選択：",
        choices=[
            "👤 Change user name",
            "📧 Change email",
            "🔑 Change password",
            "🧮 Change mode / amount",
            "💸 Change salary days",
            "⏪ Back to menu",
        ],
    ).ask()

    if choice == "👤 Change user name":
        new_name = questionary.text("新しいユーザー名：").ask()
        await auth.change_user_name(user_id, new_name)

    elif choice == "📧 Change email":
        new_email = questionary.text("新しいメールアドレス：").ask()
        await auth.change_email(user_id, new_email)

    elif choice == "🔑 Change password":
        current_pw = questionary.password("現在のパスワード：").ask()
        new_pw = questionary.password("新しいパスワード：").ask()
        confirm_pw = questionary.password("もう一度入力：").ask()
        if new_pw == confirm_pw:
            await auth.change_password(user_id, current_pw, new_pw)
        else:
            print("❌ パスワードが一致しません。")

    elif choice == "🧮 Change mode / amount":
        print("← 既存の設定変更ロジックをここに組み込み")

    elif choice == "💸 Change salary days":
        raw = questionary.text("振込日をカンマ区切りで入力 (例: 10,25)：").ask()
        salary_days = [int(x.strip()) for x in raw.split(",") if x.strip().isdigit()]
        settings = await setting_service.get_settings(user_id)
        await setting_service.set_settings(
            user_id,
            category=settings["category"],
            setting_type=settings["setting_type"],
            amount=settings["amount"],
            salary_days=salary_days,
        )
        print("✅ 給与振込日を更新しました。")
