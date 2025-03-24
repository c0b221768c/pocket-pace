import asyncio

import nest_asyncio
import questionary

from db.database import Database
from domain.services.auth_service import AuthService
from domain.services.setting_service import SettingService
from presentation.tui.app import run_tui
from shared.config import DB_CONFIG

nest_asyncio.apply()


async def main():
    db = Database(DB_CONFIG)
    await db.connect()

    auth_service = AuthService(db)
    setting_service = SettingService(db)

    user_id = None
    while not user_id:
        print("\n=== Pocket Pace CLI===")
        choice = questionary.select(
            "Choose an option:", choices=["Login", "Register", "Exit"]
        ).ask()

        if choice == "Login":
            identifier = questionary.text("Enter email or username:").ask()
            pw = questionary.password("Enter password:").ask()
            user_id = await auth_service.login_user(identifier, pw)

            if user_id:
                await setting_service.reset_alert_flags_if_needed(user_id)
                settings = await setting_service.get_settings(user_id)

                if not settings:
                    print("⚠️ Please set up your settings first.")
                    mode = questionary.select(
                        "Choose a mode:", choices=["budget", "saving"]
                    ).ask()
                    setting_type = questionary.select(
                        "Choose a amount type:", choices=["fixed", "variable"]
                    ).ask()
                    amount = int(
                        questionary.text(
                            "Enter amount for the month (budget or saving goal):"
                        ).ask()
                    )
                    salary_days = []
                    if mode == "saving":
                        raw = questionary.text(
                            "Enter salary days (comma-separated, e.g. 10,25):"
                        ).ask()
                        salary_days = [
                            int(d.strip())
                            for d in raw.split(",")
                            if d.strip().isdigit()
                        ]
                    await setting_service.set_settings(
                        user_id, mode, setting_type, amount, salary_days
                    )
                    print("✅ Settings saved.")
                await run_tui(user_id, db)

        elif choice == "Register":
            name = questionary.text("Enter your user name:").ask()
            email = questionary.text("Enter your email:").ask()
            pw = questionary.password("Enter password:").ask()
            pw_confirm = questionary.password("Confirm password:").ask()
            if pw == pw_confirm:
                await auth_service.register_user(name, email, pw)
            else:
                print("❌ Passwords do not match.")
                continue
            user_id = await auth_service.login_user(email, pw)
            print("\nFirst, let's set up your settings.")
            mode = questionary.select(
                "Choose a mode:", choices=["budget", "saving"]
            ).ask()
            setting_type = questionary.select(
                "Choose a amount type:", choices=["fixed", "variable"]
            ).ask()
            amount = int(
                questionary.text(
                    "Enter amount for the month (budget or saving goal):"
                ).ask()
            )
            salary_days = []
            if mode == "saving":
                raw = questionary.text(
                    "Enter salary days (comma-separated, e.g. 10,25):"
                ).ask()
                salary_days = [
                    int(d.strip()) for d in raw.split(",") if d.strip().isdigit()
                ]
            await setting_service.set_settings(
                user_id, mode, setting_type, amount, salary_days
            )
            print("✅ Settings saved.")
        elif choice == "Exit":
            break

    await db.close()


if __name__ == "__main__":
    asyncio.run(main())
