# GitHubリリース作成ガイド

このガイドでは、Hydro-OpsのGitHubリリースを作成する手順を説明します。

## リリースの作成手順

### 1. GitHubのWeb UIを使用する場合（推奨）

1. GitHubリポジトリのページにアクセス: https://github.com/hiromura16/HydroOps
2. 右側の「Releases」セクションをクリック
3. 「Draft a new release」をクリック
4. 以下の情報を入力：
   - **Tag version**: `v0.1.0-beta`（既にプッシュ済みのタグを選択）
   - **Release title**: `Hydro-Ops v0.1.0-beta`
   - **Description**: `.github/release-draft.md`の内容をコピー＆ペースト
   - **Pre-release**: ✅ チェック（ベータリリースの場合）
5. 「Publish release」をクリック

### 2. GitHub CLIを使用する場合

```bash
# GitHub CLIがインストールされている場合
gh release create v0.1.0-beta \
  --title "Hydro-Ops v0.1.0-beta" \
  --notes-file .github/release-draft.md \
  --prerelease
```

### 3. リリースノートの内容

リリースノートの内容は `.github/release-draft.md` に用意されています。
必要に応じて編集してください。

## リリース後の確認

リリース作成後、以下を確認してください：

- [ ] リリースページが正しく表示されているか
- [ ] タグが正しく作成されているか
- [ ] リリースノートが正しく表示されているか
- [ ] ダウンロード可能なアセットがあるか（該当する場合）

## 次のリリースの準備

新しいリリースを作成する際は：

1. `CHANGELOG.md`を更新
2. バージョン番号を更新
3. 新しいタグを作成
4. リリースノートを更新
5. リリースを作成

---

**注意**: ベータリリースの場合は、必ず「Pre-release」にチェックを入れてください。

