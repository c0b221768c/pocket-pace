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

## 2. セットアップスクリプトの使い方

このプロジェクトでは、環境構築や開発作業をスムーズに行うためのスクリプトが用意されています。

### 2.1. 初期セットアップ

初めて環境をセットアップする際には、以下のスクリプトを実行してください。

#### Mac の場合

```bash
init/setup.sh
```

#### Windows (WSL2) の場合

```bash
init/setup.bat
```

このスクリプトは、以下の処理を実行します。

- GitHub の SSH 設定
- Docker 環境のセットアップ
- その他の必要な環境構築

様々なエラーが出ると思いますが、**すべて解決**してください。
このスクリプトのエラーが無くなったら初期設定が完了します。

---

### 2.2. 毎回の起動

セットアップが完了した後は、開発環境を起動するために以下のスクリプトを実行します。

#### Mac の場合

```bash
run.sh
```

#### Windows (WSL2) の場合

```bash
run.bat
```

このスクリプトを実行すると、Docker コンテナが起動し、開発環境がセットアップされます。

---

これで `README.md` のセットアップガイドは完成です！

---

# コミットメッセージのルール

このプロジェクトでは、`commit-msg.py` スクリプトによってコミットメッセージのフォーマットが検証されます。以下のルールに従って、適切なメッセージを作成してください。

## 許可されるフォーマット

コミットメッセージは以下の形式で記述する必要があります：

```
Vx.y.z  # バージョン（1行目）
TYPE: メッセージ（2行目以降）
```

### コミットメッセージの例

```bash
git commit -m "V1.2.3"
git commit -m "FIX: バグを修正"
git commit -m "ADD: 新しい機能を追加"
git commit -m "DOCS: READMEを更新"
```

## 許可される TYPE

| タイプ | 説明 |
|--------|--------------------------------|
| ADD    | 新しい機能の追加 |
| FIX    | バグ修正 |
| UPDATE | 既存機能の更新 |
| REMOVE | 機能の削除 |
| REFACTOR | コードリファクタリング（動作の変更なし） |
| TEST   | テストの追加や修正 |
| DOCS   | ドキュメントの変更 |
| STYLE  | コードのフォーマット（動作の変更なし） |
| CHORE  | ビルドや補助ツールの変更 |

## バリデーションルール

1. **1行目にはバージョン番号を記述すること**
   - `Vx.y.z` の形式である必要があります（例: `V1.0.0`）。
2. **2行目以降は `TYPE: メッセージ` の形式で記述すること**
   - `TYPE` は上記のリストから選択してください。
   - `:` の後に**半角スペース1つ**を入れること。
   - メッセージは省略せずに記述すること。
3. **許可されていない `TYPE` は使用不可**
   - `commit-msg.py` で検証され、不正な場合はエラーとなります。
4. **空行は許可される**
   - ただし、不要な空行の挿入は避けること。

## エラーハンドリング

`pre-commit` フックを使用して、コミット時に `commit-msg.py` を実行し、メッセージの検証を行います。不正なフォーマットのメッセージは拒否され、以下のようなエラーが出力されます。

```
❌ コミットメッセージにエラーがあります:
   - 1行目のフォーマットが間違っています: 'xxx' → 'Vx.y.z' 形式にしてください
   - 2行目のフォーマットが間違っています: 'xxx' → 'TYPE: message' 形式にしてください
   - TYPE 'xxx' は許可されていません（許可: ADD, FIX, UPDATE, REMOVE, REFACTOR, TEST, DOCS, STYLE, CHORE）
```

以上のルールに従って、適切なコミットメッセージを作成してください。

