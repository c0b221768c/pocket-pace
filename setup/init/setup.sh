#!/bin/bash

set -e  # エラーが発生したらスクリプトを停止

CONTAINER_NAME="pocket-pace"
WORKSPACE_PATH="$(pwd)"
SSH_KEY="$HOME/.ssh/id_ed25519"
SSH_PUB_KEY="$SSH_KEY.pub"

### GitHub SSH のセットアップ ###
echo "🚀 GitHub の SSH 設定を開始..."

# SSH_AUTH_SOCK が設定されているか確認
if [ -z "$SSH_AUTH_SOCK" ]; then
    echo "🔄 SSHエージェントを起動します..."
    eval "$(ssh-agent -s)"
    export SSH_AUTH_SOCK
fi

# Git のメールアドレスを取得
EMAIL=$(git config --global user.email || echo "")
if [ -z "$EMAIL" ]; then
    read -p "📢 Git のメールアドレスを入力: " EMAIL
fi

# SSH キーの作成
if [ ! -f "$SSH_KEY" ]; then
    echo "🔑 SSH キーが見つかりません。新しく作成します..."
    ssh-keygen -t ed25519 -C "$EMAIL" -f "$SSH_KEY" -N ""
fi

# SSH エージェントに鍵を追加
ssh-add "$SSH_KEY"

# ~/.ssh/config 設定
SSH_CONFIG="$HOME/.ssh/config"
if [ ! -f "$SSH_CONFIG" ]; then
    echo -e "Host github.com\n    User git\n    IdentityFile ~/.ssh/id_ed25519\n    ForwardAgent yes" > "$SSH_CONFIG"
    chmod 600 "$SSH_CONFIG"
fi

# GitHub への接続テスト
echo "🔄 GitHub への接続テストを実行..."
if ssh -o StrictHostKeyChecking=no -T git@github.com 2>&1 | grep -q "You've successfully authenticated"; then
    echo "✅ GitHub への SSH 接続が成功しました！"
else
    echo "❌ GitHub への SSH 接続に失敗しました。"
    echo "🔗 GitHub に SSH 公開鍵を登録してください: https://github.com/settings/keys"
    cat "$SSH_PUB_KEY"
    exit 1
fi

### Docker 環境のセットアップ ###
echo "🐳 Docker 環境をセットアップ中..."

# Docker が起動しているか確認
if ! docker info > /dev/null 2>&1; then
    echo "🚀 Docker が起動していません。起動します..."
    open -a Docker || systemctl start docker
    sleep 10
fi

# VSCode Dev Container に接続
echo "📝 VSCode の Dev Container を開きます..."
devcontainer --version

echo "✅ 環境セットアップが完了しました！"
