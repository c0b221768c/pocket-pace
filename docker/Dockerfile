FROM ubuntu:22.04

# 環境変数設定（対話モード無効化）
ENV DEBIAN_FRONTEND=noninteractive

# シェルのエラーハンドリング強化
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt update && apt install -y git curl dos2unix
RUN curl -fsSL https://astral.sh/uv/install.sh | bash

COPY .git /app/.git
COPY startup.sh /app/startup.sh
