#!/bin/bash

echo "🔧 環境セットアップを開始します..."

# 1️⃣ GitHub SSHのセットアップ
echo "🚀 GitHubのSSH設定を実行中..."
bash "$(dirname "$0")/setup_github.sh"

if [[ $? -ne 0 ]]; then
    echo "❌ GitHub SSH設定に失敗しました。"
    exit 1
fi

# 2️⃣ Docker環境のセットアップ
echo "🐳 Docker環境をセットアップ中..."
bash "$(dirname "$0")/setup_docker.sh" $1

if [[ $? -ne 0 ]]; then
    echo "❌ Dockerセットアップに失敗しました。"
    exit 1
fi

echo "✅ 環境セットアップが完了しました！"
