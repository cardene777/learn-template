---
name: learn-deployer
description: Learn TemplateをChatGPT/AIからセットアップし、利用者自身のGitHub repository、Basic Auth、Cloudflare Workers、GitHub Actions、初回デプロイ、失敗復旧まで進めるSkill。「Learnをセットアップして」「このTemplateを自分用にデプロイして」「Cloudflareまで作って」「セットアップの続き」「Actionsが失敗しているので直して」などで使用する。ブラウザ編集は任意機能として扱い、利用者が必要とした場合だけGitHub PAT設定と編集E2Eを追加する。
---

# Learn Deployer

Learn TemplateをCloudflare Workersへセットアップします。Toolで実行できる操作は自動実行し、本人操作が必要な箇所だけをCheckpointとして案内します。

人間向け手順のSource of Truthは`docs/setup.md`です。仕様やSecret名が不明な場合は、長い手順をSkillへ複製せず`docs/setup.md`と実際のWorkflow/Workerコードを確認してください。

## Setup Mode

最初に利用者の希望と現在状態からモードを決めます。

### Standard mode

既定です。

- Basic Auth: ON
- Cloudflare Deploy: ON
- ブラウザ編集: OFF

必要Credentialは次です。

```text
CLOUDFLARE_ACCOUNT_ID
CLOUDFLARE_API_TOKEN
WORKER_BASIC_USER
WORKER_BASIC_PASSWORD
```

### Editing mode

本文編集・タイトル編集からGitHubへ保存したい場合だけ追加します。

```text
WORKER_GITHUB_TOKEN
```

GitHub PATは対象Learn repositoryだけへ限定し、最低限`Contents: Read and write`を使います。

## 成功状態

Standard modeでは次が成立したら完了です。

1. 利用者自身のGitHub repositoryがある。
2. `Astro Cloudflare Deploy`が成功している。
3. workers.devまたはCustom Domainへアクセスできる。
4. Basic Authでログインできる。
5. ヘッダーのGitHubリンクが利用者自身のrepositoryを指す。

Editing modeではさらに次を確認します。

6. `本文編集`でMarkdownを読み込める。
7. 保存すると利用者repositoryへCommitされる。
8. そのCommit後に再デプロイが成功する。

編集を使わない利用者へGitHub PATを要求しないでください。

## 最重要原則

### 現在地を読んでから動く

新規セットアップと決めつけず、利用可能なToolで次を確認します。

- 対象repositoryが存在するか。
- `.github/workflows/deploy-cloudflare.yml`があるか。
- `wrangler.jsonc`があるか。
- 直近GitHub Actions Run。
- Cloudflare Workerが既に存在するか。
- Secretの存在を確認できる場合は名前・設定有無だけ。
- 既にworkers.dev URLがあるか。

既に完了している工程は飛ばします。

### 自動実行できる操作は自動実行する

GitHub/Cloudflare操作が必要な時は、手動手順を案内する前に現在利用可能なConnector/Toolを確認します。

Toolが無い、権限が無い、本人操作が必要な場合だけManual Checkpointにします。

### Secret値をチャットへ貼らせない

GitHub PAT、Cloudflare API Token、Basic認証PasswordなどのSecret値を通常のチャットへ貼るよう依頼してはいけません。

安全なSecret書き込みToolがあれば使い、無ければGitHub/CloudflareのSecret入力UIへユーザー本人が直接登録するよう案内します。

Secret値をChat、repository file、Issue、PR、URL、Build log、Skill、eval、`PUBLIC_*`へ出力しないでください。

### 途中再開を前提にする

ユーザーが「設定した」「作った」「続きやって」と言った場合、状態を再取得して未完了Gateから続けます。最初の説明を繰り返しません。

## 実行フロー

### Phase 0. Source of Truth

`docs/setup.md`、`.github/workflows/deploy-cloudflare.yml`、`wrangler.jsonc`、`src/index.js`を確認します。

Skillと実装が食い違う場合は実際のrepository状態を優先します。

### Phase 1. Capability Discovery

最低限、次をavailable/manualに分類します。

- GitHub repository read/write
- repository作成 / Template利用
- GitHub Actions Secret write
- Workflow Run確認・再実行
- Cloudflare Worker操作
- Cloudflare Secret操作
- workers.dev疎通確認

表を毎回ユーザーへ表示する必要はありません。

### Phase 2. Repository

repositoryが無ければTemplateから作成します。Toolで作れない場合だけ`Use this template`をCheckpointとして案内します。

repositoryがあれば、必要ファイルを確認してそのまま続行します。

### Phase 3. Basic Auth

Basic Authは標準構成で必須です。

ユーザー名が未確定なら次のように1ステップずつ聞きます。

```text
Basic Authのログイン用ユーザー名を教えてください。
```

ユーザー名は通常会話で受け取って構いません。

パスワードはチャットへ送らせません。安全なSecret writerが無い場合は次のように案内します。

```text
GitHub Actions Secret `WORKER_BASIC_PASSWORD`へパスワードを直接登録してください。
値はこのチャットへ送らないでください。登録できたら「設定した」と送ってください。
```

必要に応じて`WORKER_BASIC_USER`もGitHub Actions Secretとして登録します。

### Phase 4. Cloudflare Credential

`CLOUDFLARE_ACCOUNT_ID`と`CLOUDFLARE_API_TOKEN`を確認します。

値そのものをチャットへ要求しません。安全な書き込みToolが無ければGitHub Actions Secretへの登録だけ案内します。

### Phase 5. Editing Option

ブラウザ編集を使う希望が明示されていない場合はStandard modeのまま進めます。

編集を使う場合だけFine-grained PATと`WORKER_GITHUB_TOKEN`設定へ進みます。

既にCloudflare Workerに`GITHUB_TOKEN`が保存されている場合、再登録が不要か実装と現在状態を確認してください。

### Phase 6. Repository Configuration

`wrangler.jsonc`のWorker名を確認します。同じCloudflare Account内で衝突する場合だけ変更します。

GitHub repository URLを利用者固有の固定値へSource上でハードコードしないでください。Workflowのrepository bindingを維持します。

### Phase 7. Deploy

`Astro Cloudflare Deploy`を実行します。pushで既にRunが起動していれば二重実行しません。

Runを最後まで追跡します。失敗した場合はFailed Stepとlogを確認し、repository側で修正できる問題ならbranch/PR/mergeして再実行します。

代表的な失敗は`references/troubleshooting.md`を必要な時だけ参照します。

同じ修正を証拠なしに繰り返さないでください。

### Phase 8. E2E Verification

Standard mode:

1. Siteが応答する。
2. Basic Authが有効。
3. Header GitHub linkが利用者repositoryを指す。

Editing mode:

4. 編集APIがGitHub credential不足を返さない。
5. `本文編集`でMarkdownを取得できる。
6. 保存後にGitHub Commitが作られる。
7. Commit後のDeploymentが成功する。

Basic Auth情報をブラウザToolへ安全に渡せない場合、その項目だけユーザーCheckpointにします。GitHub ActionsやDeploymentなどToolで確認できるEvidenceは自分で確認します。

## Failure Classification

必要に応じて次へ分類します。

- `repository_setup`
- `github_permission`
- `github_secret`
- `cloudflare_auth`
- `cloudflare_worker`
- `build_validation`
- `github_write_api`
- `deployment_propagation`
- `e2e_edit`

## Manual Checkpoint

長い手順を再掲せず、今必要な操作だけを提示します。

```text
GitHub側でWORKER_GITHUB_TOKENをRepository Secretとして登録してください。
値はこのチャットへ送らないでください。
登録できたら「設定した」と送ってください。
```

編集を使わない場合、このCheckpoint自体を出してはいけません。

## Output

完了時は次を簡潔に報告します。

- 対象GitHub repository
- Cloudflare Worker / URL
- Deployment成功状態
- Basic Auth確認結果
- Editing modeならGitHub write E2E結果
- 残作業があればその1点

Secret値は含めません。
