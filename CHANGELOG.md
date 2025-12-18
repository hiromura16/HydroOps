# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

