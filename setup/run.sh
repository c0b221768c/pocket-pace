#!/bin/bash

set -e  # エラー時にスクリプトを終了
export LC_ALL=C.UTF-8

echo "Starting development environment..."

# SSHエージェントの確認と起動
if ! pgrep -x "ssh-agent" > /dev/null; then
    echo "Starting SSH agent..."
    eval "$(ssh-agent -s)" > /dev/null
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to start SSH agent."
        exit 1
    fi
fi

ssh-add ~/.ssh/id_ed25519 > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to add SSH key to agent."
    exit 1
fi

# Dockerが起動しているか確認し、必要なら起動
if ! docker info > /dev/null 2>&1; then
    echo "Starting Docker..."
    open --background -a "Docker"
    sleep 10  # Dockerが起動するのを待つ

    if ! docker info > /dev/null 2>&1; then
        echo "ERROR: Failed to start Docker."
        exit 1
    fi
fi

# Dockerコンテナの起動
echo "Starting Docker container..."
docker compose up -d --build
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to start Docker container. Check the logs above for details."
    exit 1
fi

# VSCode Dev Container の起動
if command -v devcontainer > /dev/null 2>&1; then
    devcontainer open .
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to open VSCode Dev Container."
        exit 1
    fi
else
    echo "WARNING: devcontainer CLI not found. Skipping VSCode Dev Container startup."
fi

echo "Development environment started successfully."
exit 0
