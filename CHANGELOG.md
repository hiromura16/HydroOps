# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2026-05-22

### Added
- Home Assistant（Raspberry Pi）をTraefikのファイルプロバイダー経由で公開する設定を追加
  - `docker/traefik/dynamic_conf/toshi_hass.yml` 新規追加
  - Tailscale経由の内部IPへのリバースプロキシ対応

### Changed
- SSL証明書管理をJPRS有料ワイルドカード証明書からLet's Encrypt無料証明書へ移行
  - HTTP-01チャレンジによるサブドメイン個別証明書方式を採用
  - Traefik ACMEクライアントによる90日周期の自動更新に切り替え
  - 全サービスの compose.yml に `tls.certresolver=letsencrypt` ラベルを追加
  - `docker-compose.yml` の `traefik_acme_data` ボリュームを有効化
- `certs/docs/README.md` をLet's Encrypt方式に全面改訂

### Security
- 公開リポジトリ向けに具体的なドメイン名・IPアドレス・メールアドレスをプレースホルダーへ置換
- `git filter-repo` でコミット履歴全体から機密文字列を削除
- `HANDOVER.md`（社内引き継ぎ書類）を `.gitignore` に追加

### Removed
- 旧JPRS証明書の手動設定（`dynamic_conf/certificates.yml`）を無効化
- Traefikへの証明書ファイルマウント（`certs/live/`）を削除

---

## [0.1.0-beta] - 2025-12-18

### Added
- 初回ベータリリース
- Docker Composeベースの統合監視プラットフォーム
- データ収集・保存機能
  - InfluxDB時系列データベース
  - Kasen2InfluxDB河川水位データスクレイパー
  - Telegrafシステムメトリクス収集
  - Loki & Promtailログ集約システム
- モニタリング・可視化機能
  - Grafanaデータ可視化ダッシュボード
  - Prometheusメトリクス監視
  - Alertmanagerアラート管理
- 自動化・処理機能
  - Node-REDフローベースプログラミングツール
  - n8nワークフロー自動化ツール
  - Kapacitor時系列データ処理エンジン
- セキュリティ・公開機能
  - Traefikリバースプロキシ・SSL終端
  - Nginx静的コンテンツ配信
- 包括的なドキュメント
  - SETUP.md - セットアップガイド
  - DEPLOYMENT_CHECKLIST.md - デプロイメントチェックリスト
  - GIT_SETUP.md - Gitリポジトリ管理ガイド
  - certs/docs/README.md - SSL証明書管理ガイド
- セキュリティ対策
  - 機密情報の.gitignore設定
  - 設定ファイルの.exampleテンプレート
  - デプロイメントチェックリストによる設定漏れ防止

### Security
- 機密情報（ユーザーID、ドメイン名など）をプレースホルダーに置き換え
- Git履歴から機密情報を削除
- 設定ファイルのテンプレート化

### Documentation
- README.mdの整理と改善
- デプロイメントチェックリストの追加
- セットアップガイドの詳細化

[0.1.0-beta]: https://github.com/hiromura16/HydroOps/releases/tag/v0.1.0-beta

