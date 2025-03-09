import sys
from pathlib import Path
from subprocess import CalledProcessError, check_output

import toml

pyproject_path = Path(__file__).parent.parent / "pyproject.toml"


# プロジェクトのバージョンを取得
def get_project_version():
    if not pyproject_path.exists():
        print("❌ エラー: pyproject.toml が見つかりません")
        sys.exit(1)

    with open(pyproject_path, "r", encoding="utf-8") as f:
        pyproject = toml.load(f)

    try:
        return f'V{pyproject["project"]["version"]}'
    except KeyError:
        print("❌ エラー: pyproject.toml に 'project.version' が見つかりません")
        sys.exit(1)


# `git describe` から最新のタグを取得
def get_latest_git_tag():
    try:
        return check_output(
            ["git", "describe", "--tags", "--abbrev=0"], encoding="utf-8"
        ).strip()
    except CalledProcessError:
        print("⚠️ Gitタグが見つかりません。新しいタグを作成してください。")
        return None


def sync_version():
    project_version = get_project_version()
    latest_tag = get_latest_git_tag()

    if not latest_tag:
        sys.exit(1)  # タグがない場合は処理を中止

    if latest_tag == project_version:
        print("✅ バージョンが同期されています")
        sys.exit(0)

    # TOML を読み込んでバージョンを書き換える
    with open(pyproject_path, "r", encoding="utf-8") as f:
        pyproject = toml.load(f)

    pyproject["project"]["version"] = latest_tag[1:]  # `V` を除いたバージョンにする

    with open(pyproject_path, "w", encoding="utf-8") as f:
        toml.dump(pyproject, f)

    print(f"✅ バージョンを同期しました: {project_version} -> {latest_tag}")


if __name__ == "__main__":
    sync_version()
