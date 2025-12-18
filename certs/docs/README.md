# certs ディレクトリ README

このドキュメントでは、`/opt/app/<プロジェクト名>/certs/` 配下のディレクトリ構成と、SSL/TLS 証明書の管理・更新手順をまとめています。

---

## ディレクトリ構成

```
certs/
├─ chain/                   中間証明書管理用
│   └─ JPRS_DVCA_G4.pem     中間 CA 証明書（PEM 形式）
├─ csr/                     CSR（Certificate Signing Request）提出用
│   └─ yourdomain.com.csr   CA へ提出する CSR
├─ live/                    本番公開用証明書置き場
│   ├─ cert.pem             サーバ証明書（PEM 形式）
│   ├─ fullchain.pem        サーバ＋中間証明書連結ファイル
│   └─ yourdomain.com.key   プライベートキー (600, root:root)
└─ docs/                    補足ドキュメント
    └─ install_nginx.pdf    nginx インストール手順書等
```

---

## パーミッションとオーナーシップ

```
chain/JPRS_DVCA_G4.pem        owner: app-user, mode: 644
csr/yourdomain.com.csr        owner: root,        mode: 644
live/yourdomain.com.key       owner: root,        mode: 600
live/cert.pem                 owner: root,        mode: 644
live/fullchain.pem            owner: root,        mode: 644
```

---

## 更新手順

1. **CSR の作成（必要に応じて）**

   ```bash
   openssl req -new \
     -key live/yourdomain.com.key \
     -out csr/yourdomain.com.csr \
     -subj "/C=JP/ST=Tokyo/L=Chiyoda-ku/O=Example Corp/OU=IT/CN=yourdomain.com"
   ```

2. **CA へ CSR を提出**

   * `csr/yourdomain.com.csr` を証明書発行機関へアップロードし、サーバ証明書（`cert.pem`）を受領。

3. **中間証明書の更新**

   ```bash
   mv chain/JPRS_DVCA_G4.pem chain/JPRS_DVCA_G4.pem.bak
   mv <新しい中間証明書>.pem chain/JPRS_DVCA_G4.pem
   chmod 644 chain/JPRS_DVCA_G4.pem
   chown app-user:app-user chain/JPRS_DVCA_G4.pem
   ```

4. **fullchain.pem の再生成**

   ```bash
   cat live/cert.pem chain/JPRS_DVCA_G4.pem > live/fullchain.pem
   chmod 644 live/fullchain.pem
   chown root:root live/fullchain.pem
   ```

5. **Traefik の再起動**

   ```bash
   docker-compose -f /opt/app/<プロジェクト名>/docker-compose.yml restart traefik
   ```

---

## トラブルシューティング

* **証明書チェーンエラー**

  ```bash
  openssl s_client -connect yourdomain.com:443 -showcerts
  ```

  で中間証明書の提示状況を確認。

* **パーミッションエラー**
  Traefik ログに `permission denied` が出たら、`live/*.key` の所有者・パーミッションを見直す。

---

## 付録

* **証明書一覧確認**

  ```bash
  ls -l chain/ csr/ live/
  ```

* **バックアップ**
  `docs/backup/` にタイムスタンプ付きで古い証明書を保存することを推奨。

* **README 保守**
  手順やファイル名を変更したら、この README を更新してください。

*Last Updated: 2025-05-11*
