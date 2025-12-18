# セットアップガイド

このドキュメントでは、HydroOpsをGitHubリポジトリからセットアップする手順を説明します。

**重要**: デプロイ前に必ず **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** を確認し、すべてのプレースホルダーを実際の値に置き換えてください。

## 前提条件

- Gitがインストールされていること
- Docker Engine 20.10以上がインストールされていること
- Docker Compose v2.20.0以上がインストールされていること

## セットアップ手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/hiromura16/HydroOps.git
cd HydroOps
```

### 2. デプロイメントチェックリストの確認

**重要**: デプロイ前に **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** を必ず確認してください。

このチェックリストには、以下の重要な設定項目が含まれています：
- ドメイン名の設定（複数ファイル）
- 機密情報を含む設定ファイルの作成
- SSL証明書の配置
- 環境変数の設定

### 3. 機密情報を含む設定ファイルの作成

詳細は [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) の「2. 機密情報を含む設定ファイルの作成」セクションを参照してください。

### 4. SSL証明書の配置

詳細は [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) の「3. SSL証明書の配置」セクションを参照してください。

### 5. 外部ボリュームの作成

```bash
docker volume create hydro_ops_prometheus_data
docker volume create hydro_ops_kapacitor_data
```

### 6. システムの起動

すべてのチェック項目が完了したら、システムを起動します：

```bash
docker compose up -d
```

### 7. 動作確認

各サービスが正常に起動しているか確認：

```bash
docker compose ps
```

ログを確認：

```bash
docker compose logs -f [サービス名]
```

詳細な確認項目は [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) の「デプロイ後の確認」セクションを参照してください。

## トラブルシューティング

### 設定ファイルが見つからないエラー

`.example`ファイルをコピーして、実際の設定ファイルを作成してください。

### 証明書エラー

`certs/live/`ディレクトリに必要な証明書ファイルが配置されているか確認してください。

### ポート競合エラー

他のサービスが同じポートを使用している可能性があります。`docker-compose.yml`や各サービスの`compose.yml`でポート設定を確認してください。

## 次のステップ

セットアップが完了したら、以下のドキュメントを参照してください：

- [README.md](README.md) - プロジェクトの概要と各サービスの詳細な説明
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - デプロイ時の必須チェックリスト（再確認用）
- [certs/docs/README.md](certs/docs/README.md) - SSL証明書の管理方法

