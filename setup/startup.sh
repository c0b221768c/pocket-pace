#!/bin/bash

echo "🔧 Running postCreateCommand setup..."

# astral-uv同期
uv sync

# 仮想環境のアクティベート
if [ -f "/app/.venv/bin/activate" ]; then
    chmod +x /app/.venv/bin/activate
    source /app/.venv/bin/activate
    echo "✅ Virtual environment activated."
else
    echo "❌ Virtual environment not found at /app/.venv"
    exit 1
fi

# Git のワークツリーを /app に設定
if [ -d "/app/.git" ]; then
    echo "🔄 Configuring Git sparse-checkout with GIT_WORK_TREE..."
    cd /app

    # Git リポジトリを設定
    export GIT_DIR=/app/.git
    export GIT_WORK_TREE=/app

    # sparse-checkout が未設定の場合のみ設定
    if ! git config --get core.sparseCheckout; then
        git config core.worktree /app
        git sparse-checkout init --cone
        git sparse-checkout set src scripts pyproject.toml .gitignore
        echo "✅ Git sparse-checkout configured."
    else
        echo "✅ Git sparse-checkout already set."
    fi
else
    echo "⚠️ Warning: No Git repository found in /app. Skipping sparse-checkout."
fi

# pre-commit のインストール
if command -v pre-commit > /dev/null; then
    echo "✅ pre-commit found, installing hooks..."
    pre-commit install
else
    echo "❌ pre-commit not found!"
    exit 1
fi

# git ssh の確認
echo "🔄 GitHub への接続テストを実行..."
SSH_OUTPUT=$(ssh -o StrictHostKeyChecking=no -T git@github.com 2>&1)
SSH_EXIT_CODE=$?

if echo "$SSH_OUTPUT" | grep -q "You've successfully authenticated"; then
    echo "✅ GitHub への SSH 接続が成功しました！"
    exit 0
else
    echo "❌ GitHub への SSH 接続に失敗しました。"
echo "✅ postCreateCommand setup completed!"
