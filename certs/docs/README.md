# SSL/TLS 証明書管理 README

> **⚠️ 重要: 2026-05-22 に Let's Encrypt に移行済み**
>
> 証明書の手動更新作業は不要になりました。Traefik が自動で取得・更新します。
> 詳細な引き継ぎ情報は [`HANDOVER.md`](/opt/app/hydro-ops/HANDOVER.md) を参照してください。

---

## 現在の証明書管理方式（Let's Encrypt 自動管理）

| 項目 | 内容 |
|------|------|
| 発行機関 | Let's Encrypt（無料・自動） |
| 有効期間 | 90日間（自動更新） |
| 更新タイミング | 有効期限 **30日前**に Traefik が自動更新 |
| 証明書の種類 | サブドメインごとの個別証明書（HTTP-01 チャレンジ） |
| 保存場所 | Docker ボリューム `hydro_ops_traefik_acme_data`（`/letsencrypt/acme.json`） |
| 設定ファイル | `docker/traefik/traefik.yml` の `certificatesResolvers` セクション |

---

## 証明書の確認方法

### 1. Traefik ダッシュボードで確認
ブラウザで `https://traefik.yourdomain.com` にアクセス → TLS メニューから証明書状況を確認。

### 2. コマンドラインで確認

```bash
# 各サービスの証明書発行者と有効期限を確認（例: Grafana）
echo | openssl s_client -connect grafana.yourdomain.com:443 \
  -servername grafana.yourdomain.com 2>/dev/null \
  | openssl x509 -noout -issuer -dates

# 期待する出力例:
# issuer=C=US, O=Let's Encrypt, CN=R11
# notBefore=May 22 00:00:00 2026 GMT
# notAfter=Aug 20 23:59:59 2026 GMT

# acme.json の内容を確認（証明書データが入っているか）
docker exec hydro_ops_traefik ls -la /letsencrypt/
```

### 3. Traefik ログで確認

```bash
docker logs hydro_ops_traefik --tail=100 | grep -i "acme\|cert\|tls"
```

---

## 証明書が取得できない場合のトラブルシューティング

### チェックリスト

1. **ポート 80 が外部から到達可能か？**
   - HTTP-01 チャレンジには、Let's Encrypt サーバーからポート 80 へのアクセスが必要
   - ルーターやファイアウォールでポート 80 を開放しているか確認
   ```bash
   # 外部から確認（別のサーバー等から）
   curl -I http://grafana.yourdomain.com
   ```

2. **各サブドメインの DNS が正しく設定されているか？**
   - さくらインターネットの DNS 設定で、各サブドメインがサーバー IP を向いているか確認
   ```bash
   dig grafana.yourdomain.com
   ```

3. **Traefik ログにエラーがないか？**
   ```bash
   docker logs hydro_ops_traefik 2>&1 | grep -i "error\|acme\|challenge"
   ```

4. **Let's Encrypt レートリミットに引っかかっていないか？**
   - 同一ドメインで週 50 枚まで（通常は問題ない）
   - 確認: https://crt.sh/?q=yourdomain.com

### よくあるエラーと対処

| エラー | 原因 | 対処 |
|--------|------|------|
| `connection refused` on port 80 | ファイアウォールがポート 80 をブロック | UFW / iptables でポート 80 を開放 |
| `DNS: NXDOMAIN` | サブドメインの DNS 未設定 | さくらの DNS 管理でA レコード追加 |
| `too many certificates` | レートリミット超過 | 1 週間待つか staging 環境で確認 |
| `too many failed authorizations` | DNS 未設定のまま証明書取得を5回試みた | 1 時間待ってから再試行（DNS を先に設定すること） |
| `acme.json permission denied` | ファイルパーミッション問題 | `docker exec hydro_ops_traefik chmod 600 /letsencrypt/acme.json` |

---

## 旧証明書ファイル（参考情報）

2026-05-22 以前は JPRS（さくらインターネット経由）の有料ワイルドカード証明書を使用していた。

```
certs/
├─ live/                    旧証明書ファイル（参照のみ。現在は Traefik で使用していない）
│   ├─ cert.pem             旧サーバー証明書
│   ├─ fullchain.pem        旧サーバー＋中間証明書連結
│   └─ yourdomain.com.key  旧プライベートキー（600, root:root）
├─ chain/
│   └─ JPRS_DVCA_G4.pem    旧中間CA証明書
└─ csr/
    └─ yourdomain.com.csr  旧CSR
```

> これらのファイルは削除しても問題ありません（バックアップ目的で残しています）。
> 削除する場合は `certs/live/` と `certs/chain/` ディレクトリを削除してください。

---

*Last Updated: 2026-05-22（Let's Encrypt 移行）*
