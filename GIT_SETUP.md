# Gitリポジトリのセットアップ手順

このドキュメントでは、HydroOpsプロジェクトをGitHubリポジトリで管理するための手順を説明します。

## 前提条件

- GitHubアカウントを持っていること
- Gitがインストールされていること
- GitHubリポジトリ `https://github.com/hiromura16/HydroOps` が作成されていること

## セットアップ手順

### 1. Gitリポジトリの初期化

プロジェクトのルートディレクトリで以下のコマンドを実行：

```bash
cd /Users/pirosea/Projects/HydroOps
git init
```

### 2. リモートリポジトリの追加

```bash
git remote add origin https://github.com/hiromura16/HydroOps.git
```

### 3. 初回コミット

```bash
# すべてのファイルをステージング
git add .

# 初回コミット
git commit -m "Initial commit: HydroOps monitoring system setup"
```

### 4. メインブランチの設定

```bash
# ブランチ名をmainに変更（必要に応じて）
git branch -M main
```

### 5. GitHubへのプッシュ

```bash
# GitHubリポジトリにプッシュ
git push -u origin main
```

## 注意事項

### 機密情報の確認

以下のファイルは`.gitignore`で除外されているため、Gitにコミットされません：

- `docker/kasen2influxdb/config.json`
- `docker/nodered/config/settings.js`
- `docker/traefik/dashboard_users.txt`
- `certs/live/*`
- `certs/csr/*`
- `certs/chain/*`（`.gitkeep`を除く）

初回コミット前に、これらのファイルがGitに含まれていないか確認してください：

```bash
git status
```

### 既存のリポジトリと統合する場合

GitHubリポジトリが既に存在し、ファイルが含まれている場合は、以下の手順で統合できます：

```bash
# リモートの変更を取得
git fetch origin

# リモートのmainブランチとマージ
git merge origin/main --allow-unrelated-histories

# 競合があれば解決後、コミット
git commit

# プッシュ
git push origin main
```

## 今後の作業フロー

### 変更をコミット

```bash
# 変更を確認
git status

# 変更をステージング
git add [ファイル名]

# コミット
git commit -m "変更内容の説明"

# プッシュ
git push origin main
```

### ブランチの作成とマージ

```bash
# 新しいブランチを作成
git checkout -b feature/新機能名

# 変更をコミット
git add .
git commit -m "新機能の追加"

# ブランチをプッシュ
git push origin feature/新機能名

# GitHubでPull Requestを作成してマージ
```

## トラブルシューティング

### 認証エラー

GitHubへのプッシュ時に認証エラーが発生する場合は、以下のいずれかの方法で認証を設定してください：

1. **Personal Access Tokenを使用**:
   - GitHub Settings > Developer settings > Personal access tokens でトークンを作成
   - プッシュ時にトークンを使用

2. **SSH鍵を使用**:
   - SSH鍵を設定して、リモートURLをSSH形式に変更：
   ```bash
   git remote set-url origin git@github.com:hiromura16/HydroOps.git
   ```

### 大きなファイルのエラー

大きなファイル（例：PDFファイル）が含まれている場合、Git LFSを使用するか、`.gitignore`に追加してください。

