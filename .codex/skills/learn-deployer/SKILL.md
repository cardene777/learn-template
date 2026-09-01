---
name: learn-deployer
description: Learn TemplateをChatGPT/AIからセットアップし、利用者自身のGitHub repository作成・Cloudflare Workers設定・GitHub Actions Secrets・初回デプロイ・CI失敗修復・編集E2E確認まで進めるためのSkill。「Learnをセットアップして」「このTemplateを自分用にデプロイして」「Cloudflareまで作って」「デプロイの続きやって」「Actionsが失敗しているので直して」のような要求で使用する。新規セットアップだけでなく、途中まで設定済みの環境を検出して未完了部分から再開する。
---

# Learn Deployer

Learn Templateを、可能な範囲はToolで自動実行し、本人操作が必要な箇所だけを最小限の手順としてユーザーへ渡しながら、Cloudflare Workersへのデプロイと編集E2E確認まで完了させます。

人間向けセットアップ手順のSource of Truthは`docs/setup.md`です。

このSkillへCloudflare/GitHubの長い手順を複製しないでください。仕様やSecret名、必要権限を確認する必要がある時は先に`docs/setup.md`を読みます。

## 成功状態

次がすべて成立したら完了です。

1. 利用者自身が所有するGitHub repositoryがある。
2. WorkerからGitHubへ書き込む認証情報がブラウザへ露出せず、Secretとして管理されている。
3. `Astro Cloudflare Deploy`が成功している。
4. workers.devまたは設定済みCustom Domainでサイトへアクセスできる。
5. Basic認証または採用したアクセス制御でログインできる。
6. ヘッダーのGitHubリンクが利用者自身のrepositoryを指す。
7. `本文編集`でMarkdownを読み込める。
8. 保存すると利用者repositoryの`main`へCommitされる。
9. そのCommitを契機に再デプロイが成功する。

単に「Workflowが緑になった」だけで完了扱いにしないでください。

## 最重要原則

### 現在地を読んでから動く

新規セットアップと決めつけないでください。

利用可能なToolで次を確認し、既に完了している工程は飛ばします。

- 対象GitHub repositoryが既に存在するか。
- Template由来の`.github/workflows/deploy-cloudflare.yml`があるか。
- `wrangler.jsonc`があるか。
- GitHub Actionsの直近Run状態。
- Cloudflare Workerが既に存在するか。
- Secretの存在確認が可能なら、値ではなく名前・設定有無だけ。
- 既にworkers.dev URLが発行されているか。

会話から分かる情報やToolで読める情報をユーザーへ再質問しないでください。

### 自動実行できる操作は自動実行する

「この画面を開いてください」と案内する前に、現在使えるConnector/Toolで実行できないか確認します。

外部サービス操作が必要なのに適切なToolが見当たらない場合は、利用可能なPlugin/Connectorを検索できる環境なら先に検索します。

実際にToolが無い、権限が無い、または本人操作が必要な操作だけを手動Checkpointにします。

### Secret値をチャットへ貼らせない

GitHub PAT、Cloudflare API Token、Basic認証PasswordなどのSecret値を通常のチャット本文へ貼るよう依頼しないでください。

SecretをTool経由で安全に登録できる場合は、そのSecret入力機構を使います。

安全なSecret書き込みToolが無い場合は、ユーザー本人がGitHub/CloudflareのSecret入力UIへ直接登録する手順だけを案内します。

Secret値を次へ出力しないでください。

- Chat本文。
- Repository file。
- Issue / PR。
- URL。
- Build log。
- Skill / eval。
- `PUBLIC_*`環境変数。

### 途中再開を前提にする

ユーザーが「設定した」「repository作った」「続きやって」と言った場合、最初の説明を繰り返さないでください。

現在状態を再取得し、直前の未完了Gateから続行します。

## 実行フロー

### Phase 0. Source of Truthを読む

現在のrepositoryに`docs/setup.md`があれば最初に確認します。

このSkillと`docs/setup.md`が食い違う場合、実際のWorkflow・Workerコード・最新の`docs/setup.md`を確認してから判断します。

### Phase 1. Capability Discovery

現在のセッションで利用できるToolを確認します。

最低限、次のCapabilityを分類します。

| Capability | 状態 |
| --- | --- |
| GitHub repositoryの検索・読取 | available / manual |
| GitHub repositoryの新規作成 | available / manual |
| Templateからrepository作成 | available / manual |
| GitHub Actions Secretの書込 | available / manual |
| Workflow dispatch / Run確認 | available / manual |
| Cloudflare Account / Worker操作 | available / manual |
| Cloudflare Secret操作 | available / manual |
| workers.dev疎通確認 | available / manual |

この表を毎回ユーザーへ表示する必要はありません。内部の実行計画として使います。

Toolが実際に失敗した時は、エラー内容を読んでmanualへ切り替えます。

### Phase 2. Target Repositoryを確定する

次の2モードを扱います。

#### Bootstrap mode

まだ利用者repositoryが無い場合です。

1. 配布用Template repositoryを特定する。
2. Templateから利用者所有repositoryを作成する。
3. repository名とVisibilityは会話から分かれば再質問しない。
4. 不明な場合だけ確認する。

新規repository作成Toolが無ければ、`docs/setup.md`の`Use this template`手順をユーザーへ案内します。

作成後は必ず新しいrepositoryを再取得し、存在を確認してから続けます。

#### Existing repository mode

既にrepositoryがある場合です。

次を確認します。

- `.github/workflows/deploy-cloudflare.yml`。
- `wrangler.jsonc`。
- `src/index.js`。
- `docs/setup.md`。

必要ファイルが無ければ、Templateから作られたrepositoryか、古いVersionかを切り分けます。

### Phase 3. Credential Checkpoint

`docs/setup.md`を参照し、必要Credentialを確認します。

標準構成では次です。

```text
CLOUDFLARE_ACCOUNT_ID
CLOUDFLARE_API_TOKEN
WORKER_BASIC_USER
WORKER_BASIC_PASSWORD
WORKER_GITHUB_TOKEN
```

既存Cloudflare Worker Secretを再利用できる構成では、`WORKER_*`が不要な場合があります。現在のWorkflowとWorker実装を確認して判断してください。

GitHub Fine-grained PATは対象Learn repositoryだけへ限定し、必要最小限のRepository permissionを使います。

Token発行が本人操作を要求する場合は、発行画面の設定項目だけを説明し、Token値をチャットへ送らせません。

### Phase 4. Repository Configuration

必要に応じて`wrangler.jsonc`のWorker名を確認します。

Cloudflare Account内で同名Workerが問題になることをToolで確認できるなら確認します。

変更が必要ならbranch + PRなどrepositoryの通常運用に従って変更し、CIを壊さない形で反映します。

GitHub APIの接続先repositoryを固定値へ書き換えないでください。

このTemplateはデプロイ時のrepository bindingを使う前提です。現在のWorkflowを確認し、利用者repositoryへ自動的に向くことを維持します。

### Phase 5. Secret Configuration

安全なSecret書き込みToolが利用できる場合は、ユーザーの明示的な依頼範囲内で設定します。

利用できない場合は、`docs/setup.md`の対象箇所だけを短く提示してユーザーへ登録してもらいます。

Checkpoint後に「設定した」と言われたら、Secret値を聞かず、Workflow実行によって設定の正しさを検証します。

Secretの存在確認APIが使える場合でも、値を読み出そうとしないでください。

### Phase 6. Deploy

`Astro Cloudflare Deploy`を起動できるToolがあれば起動します。

pushで自動起動済みなら二重実行しません。

Runを最後まで追跡します。

成功するまで、単に「実行中です」で終了しないでください。

失敗した場合は次を行います。

1. Failed Stepを特定する。
2. Job logを読む。
3. Repository側で修正可能か判定する。
4. 修正可能ならbranch/PR/mergeして再実行する。
5. CredentialやAccount設定の問題なら、必要な本人操作だけを案内する。
6. 修正後にRunを再確認する。

代表的な失敗は`references/troubleshooting.md`を参照します。

### Phase 7. Deployment Resultを取得する

成功Runからworkers.dev URL、Worker名、Version IDなど取得可能な情報を確認します。

URLを推測しないでください。

Cloudflare側のToolが利用できる場合は、実際のWorker/Deployment状態と照合します。

### Phase 8. E2E Verification

可能な範囲で次を確認します。

1. Siteが応答する。
2. Access controlが有効。
3. Header GitHub linkが利用者repositoryを指す。
4. 編集APIがGitHub credential不足を返さない。
5. `本文編集`でsource Markdownを取得できる。
6. 保存後に利用者repositoryへCommitされる。
7. Commit後のDeploymentが成功する。

Basic認証情報などをToolへ安全に渡せずブラウザE2Eを実行できない場合は、その項目だけをユーザー確認Checkpointにします。

その場合でも、GitHub側のCommit/ActionsやCloudflare側のDeploymentなどToolで確認できる項目は自分で確認します。

## ユーザーへ質問する条件

質問は本当に解決できない入力だけに限定します。

典型的には次です。

- 新規repository名が決まっていない。
- Public/Privateの選択が必要で文脈から決められない。
- 複数Cloudflare Accountがあり、対象を特定できない。
- Worker名をユーザーが明示的に選びたい。
- 本人操作後の完了通知が必要。

Token値そのものを質問してはいけません。

## Manual Checkpointの出し方

本人操作が必要な時は、長いセットアップ手順を最初から貼り直さないでください。

今必要な操作だけを番号付きで提示します。

操作後にユーザーが送る返答も短く指定します。

例です。

```text
GitHub側でWORKER_GITHUB_TOKENをRepository Secretとして登録してください。
値はこのチャットへ送らないでください。
登録できたら「設定した」と送ってください。
```

その後は状態を再取得して続行します。

## Failure Classification

失敗は次へ分類します。

- `repository_setup`
- `github_permission`
- `github_secret`
- `cloudflare_auth`
- `cloudflare_worker`
- `build_validation`
- `browser_smoke`
- `github_write_api`
- `deployment_propagation`
- `e2e_edit`

同じエラーへ同じ修正を繰り返さないでください。

修正後も同じ分類で失敗する場合は、新しいEvidenceを取得して原因仮説を更新します。

## Output契約

進行中の返答では、ユーザーが知る必要がある次の行動だけを明確にします。

完了時は最低限次を報告します。

- 対象GitHub repository。
- Cloudflare Worker / URL。
- Deployment成功状態。
- GitHub write E2Eの確認結果。
- ユーザー側に残っている作業があればその1点。

Secret値は含めません。

## Quality Gate

完了前に次を確認します。

- Template repositoryではなく利用者repositoryへ書き込む構成になっている。
- GitHub tokenをBrowserへ渡していない。
- SecretをSource、Build output、Chatへ露出していない。
- `main`への保存後に再デプロイが動く。
- Header GitHub linkが利用者repositoryを指す。
- Workflowの成功を実際に確認した。
- E2E未確認項目を「確認済み」と表現していない。
- 手動操作が残る場合、`docs/setup.md`全体ではなく必要なCheckpointだけを案内した。
- Toolで可能な作業をユーザーへ丸投げしていない。

## 関連資料

セットアップ仕様です。

```text
docs/setup.md
```

Deployment失敗時だけ次を読みます。

```text
.codex/skills/learn-deployer/references/troubleshooting.md
```
