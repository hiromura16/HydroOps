# デプロイメントチェックリスト

このドキュメントは、HydroOpsをデプロイする際に**必ず確認・修正が必要な箇所**をチェックリスト形式でまとめています。

機密情報を削除したため、以下のすべての項目を確認し、実際の値に置き換えてください。

## 📋 デプロイ前チェックリスト

### ✅ 1. ドメイン名の設定

以下のファイルで `yourdomain.com` を実際のドメイン名に置き換えてください：

#### 1.1 Traefik証明書設定
- [ ] **`docker/traefik/dynamic_conf/certificates.yml`**
  - 8行目: `keyFile: "/etc/ssl/traefik_certs/yourdomain.com.key"` → 実際のドメイン名に変更
  - 15行目: `keyFile: "/etc/ssl/traefik_certs/yourdomain.com.key"` → 実際のドメイン名に変更

#### 1.2 証明書ファイル名
- [ ] **`certs/live/` ディレクトリ**
  - `yourdomain.com.key` → 実際のドメイン名の秘密鍵ファイル名に変更
  - 例: `example.com.key` → `tsurudensui.net.key`

#### 1.3 証明書ドキュメント
- [ ] **`certs/docs/README.md`**（参考用）
  - 14行目: `yourdomain.com.csr` → 実際のドメイン名に変更
  - 18行目: `yourdomain.com.key` → 実際のドメイン名に変更
  - 28行目: `app-user` → 実際のユーザー名に変更
  - 29行目: `yourdomain.com.csr` → 実際のドメイン名に変更
  - 30行目: `yourdomain.com.key` → 実際のドメイン名に変更
  - 43-45行目: コマンド内の `yourdomain.com` → 実際のドメイン名に変更
  - 50行目: `yourdomain.com.csr` → 実際のドメイン名に変更
  - 58行目: `app-user:app-user` → 実際のユーザー名に変更

### ✅ 2. 機密情報を含む設定ファイルの作成

以下のファイルは `.example` ファイルからコピーして作成し、実際の値を設定してください：

#### 2.1 Kasen2InfluxDB設定
- [ ] **`docker/kasen2influxdb/config.json`** を作成
  ```bash
  cp docker/kasen2influxdb/config.json.example docker/kasen2influxdb/config.json
  ```
  - [ ] `influxdb.url`: `https://influxdb.yourdomain.com/api/v2/write?org=your-org&bucket=your-bucket&precision=s`
    - `yourdomain.com` → 実際のドメイン名に変更
    - `your-org` → 実際のInfluxDB組織名に変更
    - `your-bucket` → 実際のInfluxDBバケット名に変更
  - [ ] `influxdb.token`: `YOUR_INFLUXDB_TOKEN_HERE` → 実際のInfluxDBトークンに変更

#### 2.2 Node-RED設定
- [ ] **`docker/nodered/config/settings.js`** を作成
  ```bash
  cp docker/nodered/config/settings.js.example docker/nodered/config/settings.js
  ```
  - [ ] `username`: `admin` → 実際のユーザー名に変更（または環境変数 `NR_USER` を使用）
  - [ ] `password`: `$2y$08$YOUR_HASHED_PASSWORD_HERE` → 実際のハッシュ化されたパスワードに変更
    - パスワードのハッシュ化方法:
      ```bash
      node-red admin hash-pw
      ```
      または
      ```bash
      echo $(htpasswd -nb username password) | sed -e s/\\$/\\$\\$/g
      ```

#### 2.3 Traefikダッシュボード認証設定
- [ ] **`docker/traefik/dashboard_users.txt`** を作成
  ```bash
  cp docker/traefik/dashboard_users.txt.example docker/traefik/dashboard_users.txt
  ```
  - [ ] ユーザー名とパスワードハッシュを追加
    - パスワードハッシュの生成:
      ```bash
      echo $(htpasswd -nb username password) | sed -e s/\\$/\\$\\$/g
      ```
    - 形式: `username:$apr1$xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### ✅ 3. SSL証明書の配置

- [ ] **`certs/live/` ディレクトリ**に以下のファイルを配置：
  - [ ] `cert.pem` - サーバー証明書
  - [ ] `fullchain.pem` - 証明書チェーン
  - [ ] `[実際のドメイン名].key` - 秘密鍵（例: `tsurudensui.net.key`）
    - ファイル名は `docker/traefik/dynamic_conf/certificates.yml` の設定と一致させること

### ✅ 4. 環境変数の設定

以下の環境変数が設定されているか確認してください：

- [ ] `DOMAIN_NAME` - 実際のドメイン名（例: `tsurudensui.net`）
  - Traefikのラベルで使用されます
  - 各サービスの `compose.yml` で `${DOMAIN_NAME}` として参照されます

- [ ] `TZ` - タイムゾーン（デフォルト: `Asia/Tokyo`）

### ✅ 5. その他の設定ファイルの確認

#### 5.1 Traefik設定
- [ ] **`docker/traefik/traefik.yml`** を確認
  - 必要に応じてコメントアウトされている証明書設定を有効化

#### 5.2 各サービスのcompose.yml
- [ ] 各サービスの `docker/[サービス名]/compose.yml` で `DOMAIN_NAME` 環境変数が正しく使用されているか確認
  - `nodered.${DOMAIN_NAME}`
  - `grafana.${DOMAIN_NAME}`
  - `prometheus.${DOMAIN_NAME}`
  - など

### ✅ 6. 外部ボリュームの作成

- [ ] Prometheusデータボリューム
  ```bash
  docker volume create hydro_ops_prometheus_data
  ```

- [ ] Kapacitorデータボリューム
  ```bash
  docker volume create hydro_ops_kapacitor_data
  ```

### ✅ 7. デプロイ前の最終確認

- [ ] すべての `.example` ファイルから実際の設定ファイルが作成されているか確認
- [ ] すべての `yourdomain.com` が実際のドメイン名に置き換えられているか確認
- [ ] すべての `YOUR_*` プレースホルダーが実際の値に置き換えられているか確認
- [ ] `app-user` が実際のユーザー名に置き換えられているか確認（該当ファイルのみ）
- [ ] SSL証明書ファイルが正しいファイル名で配置されているか確認
- [ ] `DOMAIN_NAME` 環境変数が設定されているか確認

## 🚀 デプロイ手順

すべてのチェック項目が完了したら、以下のコマンドでシステムを起動します：

```bash
# システムの起動
docker compose up -d

# 起動状況の確認
docker compose ps

# ログの確認（必要に応じて）
docker compose logs -f [サービス名]
```

## 🔍 デプロイ後の確認

- [ ] すべてのサービスが正常に起動しているか確認
  ```bash
  docker compose ps
  ```

- [ ] 各サービスにアクセスできるか確認
  - Grafana: `https://grafana.[実際のドメイン名]`
  - Prometheus: `https://prometheus.[実際のドメイン名]`
  - InfluxDB: `https://influxdb.[実際のドメイン名]`
  - Node-RED: `https://nodered.[実際のドメイン名]`
  - n8n: `https://n8n.[実際のドメイン名]`
  - Traefik Dashboard: `https://traefik.[実際のドメイン名]`

- [ ] SSL証明書が正しく読み込まれているか確認（ブラウザでHTTPS接続を確認）

- [ ] 認証が正しく機能しているか確認（Node-RED、Traefik Dashboardなど）

## 📝 よくある問題と解決方法

### 証明書ファイルが見つからないエラー

- `docker/traefik/dynamic_conf/certificates.yml` の `keyFile` パスが実際のファイル名と一致しているか確認
- `certs/live/` ディレクトリにファイルが存在するか確認
- ファイルのパーミッションが正しいか確認（秘密鍵は600推奨）

### ドメイン名が解決できないエラー

- `DOMAIN_NAME` 環境変数が正しく設定されているか確認
- DNS設定が正しいか確認
- Traefikのラベルで使用されているドメイン名が正しいか確認

### 認証が機能しない

- Node-RED: `settings.js` のパスワードハッシュが正しいか確認
- Traefik: `dashboard_users.txt` の形式が正しいか確認

## 🔗 関連ドキュメント

- [SETUP.md](SETUP.md) - 詳細なセットアップ手順
- [README.md](README.md) - プロジェクトの概要とドキュメント
- [certs/docs/README.md](certs/docs/README.md) - SSL証明書の管理方法

---

**重要**: このチェックリストのすべての項目を確認してからデプロイしてください。未設定の項目があると、システムが正常に動作しない可能性があります。


