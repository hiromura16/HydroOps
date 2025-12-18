# Hydro-Ops v0.1.0-beta リリースノート

## 🎉 初回ベータリリース

Hydro-Opsの初回ベータリリースです。このリリースでは、施設等の監視のためのデータ収集、監視、分析のための統合プラットフォームを提供します。

## ✨ 主な機能

### データ収集・保存
- **InfluxDB**: 時系列データベースによる効率的なデータ保存
- **Kasen2InfluxDB**: 山形県の河川砂防システムからのデータ収集
- **Telegraf**: システムメトリクスの自動収集
- **Loki & Promtail**: ログの集約と管理

### モニタリング・可視化
- **Grafana**: 柔軟なデータ可視化ダッシュボード
- **Prometheus**: メトリクス監視とアラート
- **Alertmanager**: アラートの管理と通知

### 自動化・処理
- **Node-RED**: フローベースのプログラミングによる自動化
- **n8n**: ワークフロー自動化ツール
- **Kapacitor**: 時系列データのリアルタイム処理

### セキュリティ・公開
- **Traefik**: リバースプロキシとSSL終端
- **Nginx**: 静的コンテンツの配信

## 📋 セットアップ要件

- Docker Engine 20.10以上
- Docker Compose v2.20.0以上（`include`ディレクティブをサポート）
- 基本的なLinuxコマンドの知識
- サーバーへのSSHアクセス

## 🚀 クイックスタート

1. リポジトリのクローン
   ```bash
   git clone https://github.com/hiromura16/HydroOps.git
   cd HydroOps
   ```

2. デプロイメントチェックリストの確認
   - [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)を必ず確認してください
   - すべてのプレースホルダーを実際の値に置き換えてください

3. セットアップの実行
   - [SETUP.md](SETUP.md)に従ってセットアップを進めてください

## 📚 ドキュメント

- [README.md](README.md) - プロジェクトの概要
- [SETUP.md](SETUP.md) - セットアップガイド
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - デプロイメントチェックリスト（**重要**）
- [GIT_SETUP.md](GIT_SETUP.md) - Gitリポジトリ管理ガイド
- [certs/docs/README.md](certs/docs/README.md) - SSL証明書管理ガイド

## ⚠️ 重要な注意事項

- このリリースは**ベータ版**です。本番環境での使用前に十分なテストを行ってください
- 機密情報を含む設定ファイルは`.gitignore`で除外されています
- デプロイ前に必ず[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)を確認してください
- すべてのプレースホルダー（`yourdomain.com`、`YOUR_*`など）を実際の値に置き換えてください

## 🔒 セキュリティ

- 機密情報はGit履歴から削除されています
- 設定ファイルのテンプレート（`.example`）を提供しています
- デプロイメントチェックリストで設定漏れを防止します

## 📝 変更履歴

詳細な変更履歴は[CHANGELOG.md](CHANGELOG.md)を参照してください。

## 🤝 サポート

問題や質問がある場合は、GitHubリポジトリの[Issues](https://github.com/hiromura16/HydroOps/issues)で報告してください。

## 📄 ライセンス

このプロジェクトは[MIT License](LICENSE)の下で公開されています。

Copyright (c) 2025 Hiroshi Murakami

---

**ベータリリース**: このバージョンは開発中です。フィードバックをお待ちしています！

