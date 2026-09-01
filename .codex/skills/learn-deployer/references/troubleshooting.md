# Learn Deployer Troubleshooting

通常セットアップは`docs/setup.md`をSource of Truthにし、失敗時だけこのReferenceを読みます。

## 最初に取るEvidence

- 使用中のDeployment Path: Connector / Wrangler / GitHub Actions
- 対象GitHub repository
- `wrangler.jsonc`のWorker名
- Cloudflare認証状態
- 最初の具体的なError
- 成功後ならWorker URL / Version

Secret値は取得・表示しません。

## Cloudflareアカウントが無い

デプロイを試し続けず、先にCloudflareアカウント作成をCheckpointとして案内します。

1. Cloudflareでアカウントを作成する。
2. 必要ならメール認証を完了する。
3. `作った`と返してもらう。

Passwordや認証情報はチャットへ送らせません。

## Wranglerが未認証

まず確認します。

```bash
npx --yes wrangler@4.127.1 whoami
```

未認証ならdevice loginを優先します。

```bash
npx --yes wrangler@4.127.1 login --device
```

使えない場合は通常の`wrangler login`へfallbackします。API Tokenを最初から要求しません。

## Wranglerを実行できない

実行環境に外部ネットワークが無い、CLI実行が禁止されているなどの場合です。

- Cloudflare Connector / Toolがないか再確認する。
- どちらも無ければGitHub Actionsへfallbackする。
- fallback理由を明示し、不要なCredentialを追加で要求しない。

## Direct deployでrepositoryを判定できない

`git remote origin`が無い環境では次を明示します。

```bash
LEARN_REPOSITORY=owner/repository npm run deploy:cloudflare
```

Sourceへ固定repository URLを書き込まないでください。

## Worker名が衝突する

既存Workerを上書きしないよう別名で試します。

```bash
LEARN_WORKER_NAME=my-learn npm run deploy:cloudflare
```

テスト用途では`*-test`のような明確に別のWorker名を使います。

## Basic Auth Secret不足

必要なWorker Secretは`BASIC_USER`と`BASIC_PASSWORD`です。

Passwordをチャットへ貼らせません。安全なSecret writer、Cloudflare Dashboard、またはgitignore済み`*.secrets.json`を使います。

Secret fileを使う場合:

```bash
LEARN_SECRETS_FILE=./learn.secrets.json npm run deploy:cloudflare
```

ファイルをCommitしないでください。

## Editing credential未設定

Site表示とBasic Authは成功するが編集だけ`github_token_not_configured`になる場合です。

Editing modeを使う場合だけ`GITHUB_TOKEN`を確認します。

- PATの期限
- 対象repositoryへのRepository access
- `Contents: Read and write`
- Workerが利用者repositoryを参照しているか

Standard modeではGitHub PATは不要です。

## GitHub API 401 / 403

Token値ではなくPATのRepository access / Permission / Expirationを確認します。新Tokenが必要でも値は安全なSecret入力先へ直接登録します。

## GitHub API 409 / source_changed_reload

編集中にsourceが変わった可能性があります。最新sourceを再読込し、古いSHAで強制上書きしません。

## Cloudflare API Token方式で認証失敗

GitHub Actions fallbackを使っている場合だけ次を確認します。

- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_API_TOKEN`
- Workersを編集できる権限
- Token scopeの対象Account

Wrangler OAuthが使える環境なら、不要なAPI Token方式へ固執しません。

## Astro build failure

Failed file/pathと最初の具体的Errorを確認します。Template初期状態で失敗する場合は配布Templateのregressionとして扱います。

## Header GitHub linkがTemplateを指す

直接デプロイでは`deploy:cloudflare`のrepository判定、GitHub Actionsではrepository binding Stepを確認します。

`src/index.js`、`ArticleHeader.astro`、`LibraryHeader.astro`の`__LEARN_REPOSITORY__` markerをSource上で維持します。

## Deploy後に表示が古い

Worker Versionと実際にデプロイしたCommitを確認します。新しいDeploymentが成功していない段階でキャッシュ問題と決めつけません。

## 自動デプロイが必要

Wrangler直デプロイは初回セットアップを簡単にする経路です。pushごとの自動デプロイが必要なら、Cloudflare Git integrationまたは同梱GitHub Actionsを選びます。

GitHub Actionsを使う場合だけCloudflare API CredentialをGitHub Secretsへ登録します。
