# Hydro-Ops:（バックアップ監視システム）

## 概要

Hydro-Opsは施設等の監視のためのデータの収集、監視、分析のための統合プラットフォームです。このシステムは複数のオープンソースコンポーネントを組み合わせ、Docker Composeを使用して簡単にデプロイできる環境を提供します。現在の遠方監視システムのバックアップとして開発しています。

## システム構成

Hydro-Opsは次のコンポーネントで構成されています：

- **データ収集・保存**
    - InfluxDB: 時系列データベース
    - Kasen2InfluxDB: 河川水位データスクレイパー
    - Telegraf: システムメトリクス収集
    - Loki & Promtail: ログ集約システム
- **モニタリング・可視化**
    - Grafana: データ可視化ダッシュボード
    - Prometheus: メトリクス監視
    - Alertmanager: アラート管理
- **自動化・処理**
    - Node-RED: フローベースのプログラミングツール
    - n8n: ワークフロー自動化ツール
    - Kapacitor: 時系列データ処理エンジン
- **セキュリティ・公開**
    - Traefik: リバースプロキシ・SSL終端
    - Nginx: 静的コンテンツ配信

## 前提条件

- Docker Engine 20.10以上
- Docker Compose v2.20.0以上（`include`ディレクティブをサポート）
- 基本的なLinuxコマンドの知識
- サーバーへのSSHアクセス

## クイックスタート

初めてセットアップする場合は、[SETUP.md](SETUP.md)を参照してください。
Gitリポジトリとして管理する場合は、[GIT_SETUP.md](GIT_SETUP.md)を参照してください。

## インストール手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/hiromura16/HydroOps.git
cd HydroOps
```

### 2. 外部ボリュームの作成

```bash
docker volume create hydro_ops_prometheus_data
docker volume create hydro_ops_kapacitor_data
```

### 3. 設定ファイルのカスタマイズ

各サービスの設定ファイルは `docker/[サービス名]/config/` ディレクトリにあります。必要に応じて編集してください。

**重要**: 機密情報を含む設定ファイル（`config.json`、`settings.js`、`dashboard_users.txt`など）は`.gitignore`で除外されています。初回セットアップ時は、`.example`ファイルをコピーして設定してください。

重要な設定ファイル：

- `docker/traefik/traefik.yml`: Traefikの基本設定
- `docker/influxdb/config/influxdb.conf`: InfluxDBの設定
- `docker/grafana/config/grafana.ini`: Grafanaの設定
- `docker/kasen2influxdb/config.json`: 河川データ収集の設定（`.example`ファイルをコピーして作成）
- `docker/nodered/config/settings.js`: Node-REDの設定（`.example`ファイルをコピーして作成）
- `docker/traefik/dashboard_users.txt`: Traefikダッシュボード認証設定（`.example`ファイルをコピーして作成）

### 4. SSL証明書の設定

証明書は `certs/live/` ディレクトリに配置します：

- `cert.pem`: サーバー証明書
- `fullchain.pem`: 証明書チェーン
- `yourdomain.com.key`: 秘密鍵

または、Traefikの自動証明書取得機能を利用することもできます（`docker/traefik/compose.yml`を編集）。

### 5. システムの起動

```bash
docker compose up -d
```

すべてのサービスが起動します。初回起動時はイメージのダウンロードに時間がかかる場合があります。

## 各サービスへのアクセス

Traefikの設定に基づき、各サービスは以下のURLでアクセスできます（実際のドメイン名に置き換えてください）：

- Grafana: `https://grafana.yourdomain.com`
- Prometheus: `https://prometheus.yourdomain.com`
- InfluxDB: `https://influxdb.yourdomain.com`
- Node-RED: `https://nodered.yourdomain.com`
- n8n: `https://n8n.yourdomain.com`
- Traefik Dashboard: `https://traefik.yourdomain.com`（認証が必要）

## Kasen2InfluxDBについて

Kasen2InfluxDBは山形県の河川砂防システムからデータを収集し、InfluxDBに保存するためのカスタムコンポーネントです。

### 設定方法

#### 1. InfluxDB接続設定

`docker/kasen2influxdb/config.json.example`を`config.json`にコピーし、InfluxDBの接続情報を設定します：

```bash
cp docker/kasen2influxdb/config.json.example docker/kasen2influxdb/config.json
```

`config.json`を編集して、以下の情報を設定してください：
- `influxdb.url`: InfluxDBの書き込みエンドポイントURL
- `influxdb.token`: InfluxDBの認証トークン

#### 2. 監視対象の設定

`docker/kasen2influxdb/config.csv`を編集して、監視したい河川・観測所を指定します。

CSVファイルの形式：
```csv
measurement,location,url,table_number,time_row_position,row_position
```

各列の説明：
- `measurement`: InfluxDBに保存される測定値の名前
- `location`: 観測所の場所名
- `url`: データ取得元のURL
- `table_number`: HTMLテーブルの番号
- `time_row_position`: 時刻データの行位置
- `row_position`: データの行位置

## メンテナンス方法

### システムの更新

```bash
git pull
docker compose pull
docker compose up -d
```

### ログの確認

```bash
docker compose logs -f [サービス名]
```

例：Grafanaのログを確認

```bash
docker compose logs -f grafana
```

### バックアップ

重要なデータはDockerボリュームに保存されています。定期的にバックアップすることをお勧めします：

```bash
# InfluxDBのバックアップ例
docker exec hydro_ops_influxdb influx backup /backup
```

## セキュリティに関する注意事項

**重要**: このリポジトリには機密情報を含む設定ファイルが含まれていません。以下のファイルは`.gitignore`で除外されており、初回セットアップ時に手動で作成する必要があります：

- `docker/kasen2influxdb/config.json`: InfluxDBの認証トークンを含む
- `docker/nodered/config/settings.js`: Node-REDの認証情報を含む
- `docker/traefik/dashboard_users.txt`: Traefikダッシュボードの認証情報を含む
- `certs/live/*`: SSL証明書と秘密鍵

各ファイルの`.example`ファイルを参考に、実際の設定ファイルを作成してください。

## トラブルシューティング

### サービスが起動しない場合

```bash
docker compose ps
docker compose logs [起動しないサービス名]
```

### データベース接続エラー

- InfluxDBの接続情報（URL、トークン、組織、バケット）が正しいか確認
- `docker/kasen2influxdb/config.json`が正しく設定されているか確認
- ネットワーク設定が正しいか確認
- ファイアウォール設定を確認

### Traefikでのルーティングの問題

`docker/traefik/dynamic_conf/`内の設定ファイルを確認し、ラベルが正しく設定されているか確認してください。

### 設定ファイルが見つからないエラー

機密情報を含む設定ファイル（`config.json`、`settings.js`など）が見つからない場合は、`.example`ファイルをコピーして作成してください。

## 参考リソース

- [Docker Compose公式ドキュメント](https://docs.docker.com/compose/)
- [Traefik公式ドキュメント](https://doc.traefik.io/traefik/)
- [InfluxDB公式ドキュメント](https://docs.influxdata.com/)
- [Grafana公式ドキュメント](https://grafana.com/docs/)

## ライセンス

このプロジェクトのライセンス情報については、リポジトリのLICENSEファイルを参照してください。

## サポート・貢献

問題や提案がある場合は、GitHubリポジトリのIssueを作成してください。

- リポジトリ: [https://github.com/hiromura16/HydroOps](https://github.com/hiromura16/HydroOps)

---

このドキュメントは初心者向けの説明資料として作成されました。より詳細な情報は各サービスの公式ドキュメントを参照してください。