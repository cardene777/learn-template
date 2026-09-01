---
name: learn-deployer
description: Learn TemplateをChatGPT/AIからセットアップし、Cloudflareアカウント準備、Wrangler認証、Basic Auth、Cloudflare Workersへの直接デプロイ、必要に応じたGitHub Actions自動デプロイ、失敗復旧まで進めるSkill。「Learnをセットアップして」「このTemplateをCloudflareへデプロイして」「Cloudflareアカウントから準備して」「セットアップの続き」「デプロイが失敗したので直して」などで使用する。ブラウザ編集は任意で、必要な場合だけGitHub PATを設定する。
---

# Learn Deployer

Learn TemplateをCloudflare Workersへセットアップします。**最短でデプロイできる経路を優先**し、Toolで実行できる操作は自動実行します。本人操作が必要な箇所だけCheckpointとして案内します。

人間向けSource of Truthは`docs/setup.md`です。Secret名や実装が不明な場合は、記憶ではなく`docs/setup.md`、`wrangler.jsonc`、`src/index.js`、現在のWorkflowを確認してください。

## 既定構成

- Basic Auth: ON
- Cloudflare Deploy: ON
- ブラウザ編集: OFF
- 初回デプロイ: **Wrangler直デプロイを優先**
- GitHub Actions: 自動デプロイが必要な場合のfallback

編集を使わない利用者へGitHub PATを要求しないでください。

## Deployment Pathの優先順位

次の順で使える経路を選びます。

1. Cloudflareを直接操作できるConnector / Tool
2. Wrangler CLIを実行できる環境
3. GitHub Actions

1または2が使えるのに、最初から`CLOUDFLARE_ACCOUNT_ID`や`CLOUDFLARE_API_TOKEN`をGitHub Actions Secretとして要求してはいけません。

WranglerではOAuth / device loginを優先し、Cloudflare API Tokenの発行を不要にできるなら不要にします。

## 成功状態

Standard modeでは次が成立したら完了です。

1. 利用者自身のGitHub repositoryがある。
2. Cloudflareアカウントへ認証できている。
3. Workerがデプロイされている。
4. workers.devまたはCustom Domainへアクセスできる。
5. Basic Authでログインできる。
6. ヘッダーのGitHubリンクが利用者repositoryを指す。

Editing modeではさらに次を確認します。

7. `本文編集`でMarkdownを取得できる。
8. 保存すると利用者repositoryへCommitされる。
9. 必要な自動デプロイ経路が動作する。

## 最重要原則

### 現在地を読んでから動く

利用可能なToolでrepository、Cloudflare認証状態、既存Worker、直近Deploymentを確認します。既に完了している工程は飛ばします。

### Secret値をチャットへ貼らせない

GitHub PAT、Cloudflare API Token、Basic Auth Passwordなどを通常チャットへ貼るよう依頼してはいけません。

安全なSecret writerがある場合はそれを使います。無い場合はCloudflare Dashboard、GitHub Secret UI、またはユーザー自身のローカルでgitignoreされたSecret fileへ直接入力してもらいます。

Secret値をChat、repository、Issue、PR、URL、Build log、Skill、eval、`PUBLIC_*`へ出力しません。

### Manual Checkpointは今必要な1工程だけ

長い手順を毎回再掲しません。ユーザーが「作った」「認証した」「設定した」と返したら状態を再取得し、未完了Gateから続行します。

## Phase 0. Repositoryを確認する

対象GitHub repositoryを取得し、最低限次を確認します。

- `package.json`
- `scripts/prepare-astro.mjs`
- `wrangler.jsonc`
- `src/index.js`
- `docs/setup.md`

repositoryが無ければTemplateから作成します。Toolで作れない場合だけ`Use this template`をCheckpointとして案内します。

## Phase 1. Cloudflare Readiness

**最初にCloudflareアカウントと認証の準備状況を確認します。**

Cloudflare ConnectorがあればAccount一覧などを読みます。Wranglerが使える場合は、例えば次で認証状態を確認します。

```bash
npx --yes wrangler@4.127.1 whoami
```

### Cloudflareアカウントが無い場合

デプロイ手順へ進む前に、次だけをユーザーへ表示します。

1. Cloudflareのサインアップ画面でアカウントを作成する。
2. 必要ならメール認証を完了する。
3. 完了したらこのチャットへ`作った`と送る。

PasswordやCloudflareの認証情報をチャットへ送らせません。

### アカウントはあるがWrangler未認証の場合

remote / agent環境でdevice loginが使えるなら次を実行します。

```bash
npx --yes wrangler@4.127.1 login --device
```

表示されたCloudflare認証画面をユーザーに開いてもらい、コード承認だけを依頼します。承認後は`whoami`で確認します。

`--device`が利用できない環境では通常のOAuth loginを試します。

```bash
npx --yes wrangler@4.127.1 login
```

API Token方式は、OAuth / Connectorが使えない場合のfallbackです。

## Phase 2. Worker名を決める

`wrangler.jsonc`の既定名を確認します。既存Workerを上書きする可能性がある場合は別名を使います。

直接デプロイではSourceを書き換えず、環境変数で一時的なWorker名を指定できます。

```bash
LEARN_WORKER_NAME=my-learn npm run deploy:cloudflare
```

`LEARN_WORKER_NAME`を指定しなければ`wrangler.jsonc`の名前を使います。

## Phase 3. Basic Auth Secretを準備する

Basic Authは標準で必須です。

必要なWorker Secretは次です。

```text
BASIC_USER
BASIC_PASSWORD
```

ユーザー名は会話で決めても構いませんが、Passwordはチャットへ貼らせません。

Cloudflare Secretを安全に書き込めるToolがあれば直接登録します。

安全なSecret writerが無いがユーザーのローカルfilesystemを使える場合は、gitignore済みの`*.secrets.json`へユーザー自身が値を入力する方法を使えます。例:

```json
{
  "BASIC_USER": "<username>",
  "BASIC_PASSWORD": "<password>"
}
```

このファイルをCommitしてはいけません。デプロイ時だけ次のように指定します。

```bash
LEARN_SECRETS_FILE=./learn.secrets.json npm run deploy:cloudflare
```

デプロイ完了後は不要なら削除します。

## Phase 4. Editing Option

ブラウザ編集を使う場合だけ`GITHUB_TOKEN`をWorker Secretへ追加します。

Fine-grained PATは利用者のLearn repositoryだけを対象にし、最低限`Contents: Read and write`を付与します。

Secret file方式なら次の形です。

```json
{
  "BASIC_USER": "<username>",
  "BASIC_PASSWORD": "<password>",
  "GITHUB_TOKEN": "<fine-grained PAT>"
}
```

PAT値をチャットへ送らせません。

## Phase 5. Wrangler Direct Deploy

Wranglerが利用でき、Cloudflare認証済みなら**これを標準経路**にします。

初回だけ依存関係を入れます。

```bash
npm install
```

repository URLは通常`git remote origin`から自動判定されます。判定できない場合だけ次を指定します。

```bash
LEARN_REPOSITORY=owner/repository npm run deploy:cloudflare
```

通常の直接デプロイ:

```bash
npm run deploy:cloudflare
```

Worker名とSecret fileを指定する例:

```bash
LEARN_WORKER_NAME=my-learn \
LEARN_SECRETS_FILE=./learn.secrets.json \
npm run deploy:cloudflare
```

`deploy:cloudflare`はデプロイ時だけGitHub repository bindingとWorker名を一時適用し、build + Wrangler deploy後にSourceを元へ戻します。

Wrangler出力から実際のWorker名、Version、workers.dev URLを取得します。URLを推測しません。

## Phase 6. GitHub Actions Fallback

Wranglerを実行できない、または利用者がpushごとの自動デプロイを明示的に希望する場合だけGitHub Actionsを使います。

この場合はGitHub Actions側に次が必要です。

```text
CLOUDFLARE_ACCOUNT_ID
CLOUDFLARE_API_TOKEN
WORKER_BASIC_USER
WORKER_BASIC_PASSWORD
```

編集する場合だけ追加します。

```text
WORKER_GITHUB_TOKEN
```

Secret値はGitHub Secret UIへ直接登録します。

GitHub Actionsが失敗した場合はFailed Step / Job logを読み、repository側で直せる問題ならbranch + PR + mergeして再実行します。代表的な失敗だけ`references/troubleshooting.md`を参照します。

## Phase 7. E2E Verification

Standard mode:

1. workers.dev / Custom Domainが応答する。
2. Basic Authが有効。
3. 正しいCredentialでページが表示される。
4. Header GitHub linkが利用者repositoryを指す。

Editing mode:

5. 編集APIがGitHub credential不足を返さない。
6. `本文編集`でMarkdownを取得できる。
7. 保存後にGitHub Commitが作られる。
8. 自動デプロイを設定した場合はCommit後のDeploymentも成功する。

Basic Auth PasswordをBrowser Toolへ安全に渡せない場合、その確認だけユーザーCheckpointにします。他のEvidenceはToolで確認します。

## Failure Classification

必要に応じて次へ分類します。

- `repository_setup`
- `cloudflare_account`
- `cloudflare_login`
- `cloudflare_auth`
- `cloudflare_worker`
- `build_validation`
- `github_permission`
- `github_secret`
- `github_write_api`
- `deployment_propagation`
- `e2e_edit`

## Output

完了時は次を簡潔に報告します。

- 対象GitHub repository
- 使用したDeployment Path（Connector / Wrangler / GitHub Actions）
- Cloudflare Worker / URL
- Deployment成功状態
- Basic Auth確認結果
- Editing modeならGitHub write結果
- 残作業があればその1点

Secret値は含めません。
