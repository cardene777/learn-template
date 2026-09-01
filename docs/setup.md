# Learn Template セットアップ

このドキュメントは、Templateから自分のLearnを作り、Basic Auth付きでCloudflare Workersへデプロイするための手順です。

## ChatGPTから進める

このrepositoryにはセットアップ用Skillがあります。

```text
.codex/skills/learn-deployer/SKILL.md
```

ChatGPTへrepository URLと一緒に次のように依頼してください。

```text
このGitHub repositoryを使ってください:
https://github.com/<YOUR_NAME>/<YOUR_REPOSITORY>

repository内の .codex/skills/learn-deployer/SKILL.md を使って、
このLearnを自分用にセットアップしてCloudflareへデプロイまで進めて。
```

途中まで設定済みなら、次のように依頼すれば現在地から再開できます。

```text
learn-deployerを使って、現在の状態を確認してセットアップの続きを進めて。
```

GitHub PAT、Cloudflare API Token、Basic AuthのパスワードなどのSecret値は通常のチャットへ貼らないでください。

## 構成

初期状態のおすすめは次です。

```text
Basic Auth        ON
ブラウザ編集      OFF
Cloudflare Deploy ON
```

ブラウザ編集を使わない場合、GitHub PATは不要です。

## 1. Templateからrepositoryを作る

Public Template repositoryで`Use this template`→`Create a new repository`を選びます。

ノートを非公開にしたい場合は、作成先repositoryをPrivateにすることを推奨します。

## 2. CloudflareのCredentialを用意する

GitHub ActionsからCloudflare Workersへデプロイするため、次の2値が必要です。

```text
CLOUDFLARE_ACCOUNT_ID
CLOUDFLARE_API_TOKEN
```

Cloudflare API TokenはWorkersを編集できる必要最小限の権限にし、対象Accountへscopeを限定してください。

## 3. Basic Authを設定する

Basic Authは標準で使います。

まずログイン用ユーザー名を決めます。ChatGPTからセットアップしている場合、ユーザー名は通常の会話で指定して構いません。

次にパスワードを決めます。**パスワードはチャットへ貼らず、GitHub Actions Secretへ直接登録してください。**

自分のrepositoryで`Settings`→`Secrets and variables`→`Actions`→`Repository secrets`へ進み、次を登録します。

| Secret | 必須 | 用途 |
| --- | --- | --- |
| `CLOUDFLARE_ACCOUNT_ID` | 必須 | Cloudflare Account |
| `CLOUDFLARE_API_TOKEN` | 必須 | Workerデプロイ |
| `WORKER_BASIC_USER` | 初回セットアップでは必須 | Basic Authユーザー名 |
| `WORKER_BASIC_PASSWORD` | 初回セットアップでは必須 | Basic Authパスワード |

`WORKER_BASIC_USER`と`WORKER_BASIC_PASSWORD`は必ず2つセットで登録します。

WorkflowはCloudflare Worker Secretとして次の名前で保存します。

```text
BASIC_USER
BASIC_PASSWORD
```

一度Cloudflare側へ保存された後の再デプロイでは、既存Secretをそのまま再利用できます。

## 4. ブラウザ編集を使う場合だけGitHub PATを設定する

本文編集・タイトル編集からGitHub repositoryへCommitしたい場合だけFine-grained PATを作ります。

Repository accessは自分のLearn repositoryだけに限定し、Repository permissionsは最低限`Contents: Read and write`を付けます。

発行したPATはチャットへ貼らず、GitHub Actions Secretへ直接登録します。

| Secret | 必須 | 用途 |
| --- | --- | --- |
| `WORKER_GITHUB_TOKEN` | 編集する場合のみ | WorkerからGitHubへCommit |

WorkflowはCloudflare Worker Secret `GITHUB_TOKEN`として保存します。

編集を使わない場合、`WORKER_GITHUB_TOKEN`は設定しなくて構いません。

## 5. Worker名を確認する

デフォルトWorker名は`learn`です。

同じCloudflare Accountですでに使われている場合は`wrangler.jsonc`の`name`を変更してください。

```json
{
  "name": "my-learn"
}
```

## 6. デプロイする

GitHubの`Actions`→`Astro Cloudflare Deploy`→`Run workflow`を実行します。

Workflowは次だけを行います。

1. repository URLを現在のrepositoryへバインドする。
2. 依存関係をインストールする。
3. Astroをbuildする。
4. 設定済みWorker SecretをCloudflareへ渡す。
5. Cloudflare Workersへデプロイする。

Private開発元で行っているブラウザSmoke TestやPDF検証などはPublic Templateの通常デプロイでは実行しません。

## 7. 動作確認

デプロイ後は最低限、次を確認します。

- workers.devまたはCustom Domainへアクセスできる。
- Basic Authでログインできる。
- デザインとサンプルノートが表示される。
- ヘッダーのGitHubリンクが自分のrepositoryを指す。

ブラウザ編集を有効にした場合だけ追加で確認します。

- `本文編集`でMarkdownを読み込める。
- 保存すると自分のrepositoryへCommitされる。
- Commit後にGitHub Actionsが再デプロイする。

## Secret一覧

最小構成は4つです。

```text
CLOUDFLARE_ACCOUNT_ID
CLOUDFLARE_API_TOKEN
WORKER_BASIC_USER
WORKER_BASIC_PASSWORD
```

編集を使う時だけ次を追加します。

```text
WORKER_GITHUB_TOKEN
```

## ローカル開発

```bash
npm install
npm run dev
```

`.env`、`.dev.vars`、TokenやPasswordを含むローカルファイルはCommitしないでください。

## 問題が起きた場合

ChatGPTへrepository URLを渡し、次のように依頼できます。

```text
このGitHub repositoryのCloudflareデプロイが失敗している。
learn-deployerを使って原因を確認し、続きから直して。
```

`learn-deployer`はWorkflow Runと失敗Stepを確認し、repository側で直せる問題は修正し、Credential入力など本人操作が必要な場合だけ現在のCheckpointを案内します。
