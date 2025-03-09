FROM ubuntu:22.04

# 環境変数設定（対話モード無効化）
ENV DEBIAN_FRONTEND=noninteractive

# シェルのエラーハンドリング強化
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt update && apt install -y git curl
RUN curl -fsSL https://astral.sh/uv/install.sh | bash

COPY .git /app/.git