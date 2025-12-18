# セットアップガイド

このドキュメントでは、HydroOpsをGitHubリポジトリからセットアップする手順を説明します。

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

### 2. 機密情報を含む設定ファイルの作成

以下のファイルを`.example`ファイルからコピーして作成し、実際の値を設定してください：

```bash
# Kasen2InfluxDBの設定
cp docker/kasen2influxdb/config.json.example docker/kasen2influxdb/config.json
# エディタで docker/kasen2influxdb/config.json を編集

# Node-REDの設定
cp docker/nodered/config/settings.js.example docker/nodered/config/settings.js
# エディタで docker/nodered/config/settings.js を編集

# Traefikダッシュボード認証設定
cp docker/traefik/dashboard_users.txt.example docker/traefik/dashboard_users.txt
# エディタで docker/traefik/dashboard_users.txt を編集
```

### 3. SSL証明書の配置

`certs/live/`ディレクトリに以下のファイルを配置してください：

- `cert.pem`: サーバー証明書
- `fullchain.pem`: 証明書チェーン
- `yourdomain.com.key`: 秘密鍵（実際のドメイン名に置き換えてください）

詳細は`certs/docs/README.md`を参照してください。

### 4. 外部ボリュームの作成

```bash
docker volume create hydro_ops_prometheus_data
docker volume create hydro_ops_kapacitor_data
```

### 5. システムの起動

```bash
docker compose up -d
```

### 6. 動作確認

各サービスが正常に起動しているか確認：

```bash
docker compose ps
```

ログを確認：

```bash
docker compose logs -f [サービス名]
```

## トラブルシューティング

### 設定ファイルが見つからないエラー

`.example`ファイルをコピーして、実際の設定ファイルを作成してください。

### 証明書エラー

`certs/live/`ディレクトリに必要な証明書ファイルが配置されているか確認してください。

### ポート競合エラー

他のサービスが同じポートを使用している可能性があります。`docker-compose.yml`や各サービスの`compose.yml`でポート設定を確認してください。

## 次のステップ

セットアップが完了したら、`README.md`を参照して各サービスの設定をカスタマイズしてください。

