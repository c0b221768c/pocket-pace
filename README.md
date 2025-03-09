# Pocket Pace 環境セットアップガイド

このプロジェクトでは、開発環境のセットアップを簡単に行うために、複数のスクリプトが用意されています。本ドキュメントでは、それらのスクリプトの役割と使い方を説明します。

## 1. 事前準備

### 1.1. Devcontainer CLI のインストール

このプロジェクトでは、VSCode の Dev Container を使用するため、`devcontainer` CLI が必要です。以下のコマンドでインストールしてください。

```bash
npm install -g @devcontainers/cli
```

インストール後、以下のコマンドで正しく動作するか確認してください。

```bash
devcontainer --version
```

---

## 2. セットアップスクリプトの概要

| スクリプト | 説明 |
|------------|--------------------------|
| `setup_all.sh` | 全てのセットアップを実行（GitHub SSH、Docker） |
| `setup_github.sh` | GitHub SSH 設定を行う |
| `setup_docker.sh` | Docker環境を構築し、VSCodeのDev Containerを起動 |
| `startup.sh` | Dev Container の起動後に実行されるセットアップ処理 |

---

## 3. セットアップ手順

### 3.1. 環境を一括でセットアップする (`setup_all.sh`)

開発環境のセットアップを一括で実行したい場合は、以下のコマンドを実行してください。

```bash
bash setup/setup_all.sh
```

このスクリプトは以下の処理を行います：
1. `setup_github.sh` を実行し、GitHub の SSH 設定を行う
2. `setup_docker.sh` を実行し、Dockerコンテナを構築・起動する

---

### 3.2. GitHub SSH 設定 (`setup_github.sh`)

GitHub に SSH でアクセスできるように設定するには、以下のコマンドを実行します。

```bash
bash setup/setup_github.sh
```

このスクリプトは以下の処理を行います：
- SSH エージェントの起動
- SSH キーの作成（存在しない場合）
- `~/.ssh/config` の設定
- GitHub への接続確認

もし、GitHub への接続が成功しなかった場合は、スクリプトの指示に従って `SSH 公開鍵を GitHub に登録` してください。

---

### 3.3. Docker 環境のセットアップ (`setup_docker.sh`)

Docker 環境をセットアップし、VSCode の Dev Container を開くには、以下のコマンドを実行します。

```bash
bash setup/setup_docker.sh
```

このスクリプトは以下の処理を行います：
- Docker が起動しているか確認し、必要なら起動
- `docker compose` を使ってコンテナをビルド&起動
- VSCode の Dev Container を開く

---

## 4. Dev Container のセットアップ (`startup.sh`)

VSCode の Dev Container を開いた後、必要な環境を整えるために `startup.sh` が実行されます。

このスクリプトは以下の処理を行います：
- 仮想環境の同期 (`uv sync`)
- Python の仮想環境を有効化
- Git の sparse-checkout 設定
- `pre-commit` のインストールとセットアップ
- GitHub SSH 接続の確認

Dev Container が正しく動作しない場合は、ターミナルで手動実行することも可能です。

```bash
bash setup/startup.sh
```

---

## 5. トラブルシューティング

### 5.1. GitHub SSH 接続に失敗する
- `setup_github.sh` を実行して SSH 設定を確認
- `ssh -T git@github.com` を実行して、接続が成功するか確認
- 必要なら GitHub に SSH 公開鍵を登録

### 5.2. Docker コンテナが起動しない
- `docker ps` でコンテナが起動しているか確認
- `docker compose up --build -d` を手動で実行
- `docker logs pocket-pace` でエラーを確認

---

以上で Pocket Pace のセットアップが完了します！ 🚀

