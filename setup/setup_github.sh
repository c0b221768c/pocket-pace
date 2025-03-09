#!/bin/bash

# SSHキーの設定
SSH_KEY="$HOME/.ssh/id_ed25519"
SSH_PUB_KEY="$SSH_KEY.pub"

echo "🔧 GitHub SSH 設定を開始..."

# 1️⃣ SSH_AUTH_SOCK が設定されているか確認
if [ -z "$SSH_AUTH_SOCK" ]; then
    echo "❌ SSH_AUTH_SOCK が設定されていません！"
    echo "🔄 SSHエージェントを起動します..."
    eval "$(ssh-agent -s)"
    export SSH_AUTH_SOCK
fi

# 2️⃣ Git のメールアドレスを取得
EMAIL=$(git config --global user.email)
if [ -z "$EMAIL" ]; then
    echo "📢 Git のメールアドレスが設定されていません。手動で入力してください。"
    read -p "メールアドレスを入力: " EMAIL
fi

# 3️⃣ SSH キーがない場合は作成
if [ ! -f "$SSH_KEY" ]; then
    echo "🔑 SSH キーが見つかりません。新しく作成します..."
    ssh-keygen -t ed25519 -C "$EMAIL" -f "$SSH_KEY" -N ""
    echo "✅ SSH キーを作成しました: $SSH_KEY"
else
    echo "✅ SSH キーは既に存在します: $SSH_KEY"
fi

# 4️⃣ SSH エージェントに鍵を追加
echo "🚀 SSH エージェントに鍵を追加..."
ssh-add "$SSH_KEY"

# 5️⃣ `~/.ssh/config` に ForwardAgent を設定
SSH_CONFIG="$HOME/.ssh/config"
if [ ! -f "$SSH_CONFIG" ]; then
    echo "🔧 ~/.ssh/config が見つかりません。新しく作成します..."
    mkdir -p "$HOME/.ssh"
    echo -e "Host github.com\n    User git\n    IdentityFile ~/.ssh/id_ed25519\n    ForwardAgent yes" > "$SSH_CONFIG"
    chmod 600 "$SSH_CONFIG"
    echo "✅ ~/.ssh/config を作成しました。"
else
    echo "✅ ~/.ssh/config は既に存在します。"
fi

# 6️⃣ GitHub への接続テスト
echo "🔄 GitHub への接続テストを実行..."
SSH_OUTPUT=$(ssh -o StrictHostKeyChecking=no -T git@github.com 2>&1)
SSH_EXIT_CODE=$?

if echo "$SSH_OUTPUT" | grep -q "You've successfully authenticated"; then
    echo "✅ GitHub への SSH 接続が成功しました！"
    exit 0
else
    echo "❌ GitHub への SSH 接続に失敗しました。"
    echo "📢 SSH 公開鍵を GitHub に登録してください:"
    echo "🔗 GitHub の SSH 設定: https://github.com/settings/keys"

    # 公開鍵をクリップボードにコピー（WSL & Mac 両方対応）
    if command -v clip.exe >/dev/null 2>&1; then
        cat "$SSH_PUB_KEY" | clip.exe  # WSL2用
    elif command -v xclip >/dev/null 2>&1; then
        cat "$SSH_PUB_KEY" | xclip -selection clipboard  # Linux用
    fi

    echo "📢 公開鍵をクリップボードにコピーしました（WSL2またはLinux環境の場合）。"
    echo "🔄 GitHub に SSH キーを登録したら、以下のコマンドで接続テストをしてください:"
    echo "    ssh -T git@github.com"
    exit 1
fi
