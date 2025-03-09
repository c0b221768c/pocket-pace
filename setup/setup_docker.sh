#!/bin/bash

# 設定
CONTAINER_NAME="pocket-pace"
WORKSPACE_PATH="$(pwd)"

echo "🔧 Docker環境をセットアップ中..."

# OSの判定
if grep -qEi "(Microsoft|WSL)" /proc/version &> /dev/null; then
    PLATFORM="WSL2"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="Mac"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLATFORM="Linux"
else
    echo "❌ 未対応のOSです。スクリプトを終了します。"
    exit 1
fi

# Dockerが起動しているか確認
if ! docker info > /dev/null 2>&1; then
    echo "🚀 Dockerが起動していません。"

    if [ "$PLATFORM" == "WSL2" ]; then
        echo "🔄 Windows 側の Docker Desktop を起動します..."
        powershell.exe -Command "Start-Process 'Docker Desktop' -Verb runAs"
        echo "⏳ Docker Desktop が完全に起動するまで待機 (10秒)"
        sleep 10
    elif [ "$PLATFORM" == "Mac" ]; then
        echo "🔄 Mac で Docker Desktop を起動します..."
        open -a Docker
        sleep 10
    elif [ "$PLATFORM" == "Linux" ]; then
        echo "🔄 Linux で Docker を起動します..."
        sudo systemctl start docker
        sleep 10
    fi
fi

# コンテナが起動中か確認
if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "✅ コンテナはすでに起動しています。"
else
    echo "🔄 コンテナが起動していません。起動します..."
    docker compose up --build -d
    sleep 5
fi

# VSCode の Dev Container に接続
echo "📝 VSCode の Dev Container を開きます..."
devcontainer open "$WORKSPACE_PATH"
