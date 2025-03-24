import questionary

from presentation.tui.pages import history_page, home_page, report_page, settings_page


async def run_tui(user_id: int, db):
    current_page = "home"

    while True:
        # === 各ページ描画 ===
        if current_page == "home":
            await home_page.render(user_id, db)
        elif current_page == "report":
            await report_page.render(user_id, db)
        elif current_page == "history":
            await history_page.render(user_id, db)
        elif current_page == "settings":
            await settings_page.render(user_id, db)
        elif current_page == "logout":
            print("👋 ログアウトしました。")
            break

        # === メニュー表示（questionary）===
        current_marker = {
            "home": "🏠 Home",
            "report": "📈 Report",
            "history": "📜 History",
            "settings": "⚙️ Settings",
            "logout": "🚪 Logout",
        }

        choice = questionary.select(
            "\n📚 メニューを選択してください：", choices=list(current_marker.values())
        ).ask()

        reverse_map = {v: k for k, v in current_marker.items()}
        current_page = reverse_map.get(choice, current_page)
