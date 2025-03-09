import re
import sys

# 許可する TYPE のリスト
ALLOWED_TYPES = {
    "ADD",
    "FIX",
    "UPDATE",
    "REMOVE",
    "REFACTOR",
    "TEST",
    "DOCS",
    "STYLE",
    "CHORE",
}

# 正規表現
VERSION_REGEX = r"^V\d+\.\d+\.\d+$"
TYPE_REGEX = r"^([A-Z]+): [^\s].*$"  # TYPE: の後に半角スペース1つが必須


def check_commit_message(commit_msg_file):
    with open(commit_msg_file, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]

    if not lines:
        print("❌ エラー: コミットメッセージが空です")
        sys.exit(1)

    errors = []

    # 1行目はバージョン番号
    if not re.match(VERSION_REGEX, lines[0]):
        errors.append(
            f"1行目のフォーマットが間違っています: '{lines[0]}' → 'Vx.y.z' 形式にしてください"
        )

    # 2行目以降の `TYPE: メッセージ` チェック
    for i, line in enumerate(lines[1:], start=2):
        if not line:
            continue  # 空行はスキップ

        match = re.match(TYPE_REGEX, line)
        if not match:
            errors.append(
                f"{i}行目のフォーマットが間違っています: '{line}' → 'TYPE: message' 形式にしてください（コロンの後は半角スペース1つ）"
            )
            continue

        commit_type = match.group(1)
        if commit_type not in ALLOWED_TYPES:
            errors.append(
                f"{i}行目の TYPE '{commit_type}' は許可されていません（許可: {', '.join(ALLOWED_TYPES)}）"
            )

    if errors:
        print("❌ コミットメッセージにエラーがあります:")
        for error in errors:
            print(f"   - {error}")
        sys.exit(1)

    print("✅ コミットメッセージのチェックを通過しました")


if __name__ == "__main__":
    commit_msg_file = sys.argv[1]
    check_commit_message(commit_msg_file)
