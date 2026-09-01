# Learn Deployer Troubleshooting

DeploymentまたはEditing modeのE2Eが失敗した時だけ読みます。通常セットアップは`docs/setup.md`をSource of Truthにします。

## Evidence

推測で直さず、まず次を確認します。

1. Workflow Run ID
2. Failed Job / Step
3. 最初の具体的なErrorとlog末尾
4. 対象Commit SHA
5. `wrangler.jsonc`のWorker名
6. Deployment成功後ならWorker URL / Version ID

Secret値は取得・表示しません。

## Cloudflare Credential不足

代表例:

```text
Missing GitHub secret: CLOUDFLARE_API_TOKEN
Missing GitHub secret: CLOUDFLARE_ACCOUNT_ID
```

対象Secret名だけを案内し、値はチャットへ貼らせません。登録後にWorkflowを再実行して検証します。

## Basic Auth Secret

`WORKER_BASIC_USER`と`WORKER_BASIC_PASSWORD`はペアです。片方だけ設定されている場合はWorkflowが失敗します。

新規セットアップでは両方をGitHub Actions Secretへ登録します。既存Workerに`BASIC_USER` / `BASIC_PASSWORD`が保存済みの場合は、現在のWorkflowが既存Secretを再利用できるか確認します。

## Editing credential未設定

Site表示とBasic Authは成功するが本文編集だけ失敗し、`github_token_not_configured`などが返る場合です。

Editing modeを使う場合だけ次を確認します。

- `WORKER_GITHUB_TOKEN`が設定されているか
- Fine-grained PATの期限
- 対象repositoryへのRepository access
- `Contents: Read and write`
- Workerが利用者repositoryを参照しているか

Standard modeではこのSecretは不要です。編集を使わない利用者へ設定を要求しません。

## GitHub API 401 / 403

Token値ではなく、PATのRepository access / Permission / Expirationを本人に確認してもらいます。新Tokenが必要でも値はSecret UIへ直接登録します。

## GitHub API 409 / source_changed_reload

編集中にsourceが変わった可能性があります。最新sourceを再読込し、古いSHAで強制上書きしません。

## Cloudflare authentication failure

次を確認します。

- Account IDが対象Accountか
- API TokenがWorkersを編集できるか
- Token scopeが対象Accountを含むか
- Wranglerの具体的なerror code/message

複数Accountがある場合は推測で選びません。

## Worker name conflict

`wrangler.jsonc`の`name`が既存Workerと衝突する場合は利用者専用名へ変更します。Deployment URLは推測せずWrangler出力から取得します。

## Astro build failure

Failed file/pathと最初の具体的Errorを確認します。Validationを無効化して通すのではなく、sourceを修正します。

Template初期状態で失敗する場合は配布Templateのregressionとして扱います。

## Header GitHub linkがTemplateを指す

`.github/workflows/deploy-cloudflare.yml`のrepository bindingと、Header component / Worker内の`__LEARN_REPOSITORY__` markerを確認します。

利用者repositoryへ自動bindingする設計を維持し、固定URLを手作業で書き換える運用へ戻しません。

## Deploy後に表示が古い

対象Commit SHA、Worker Version、最新Workflow Runを確認します。新しいRunが成功していない段階でキャッシュ問題と決めつけません。

## Editing保存後に再デプロイされない

- Commit先が`main`か
- Workflowの`on.push.branches`
- `paths`に変更したcontent fileが含まれるか
- Commitが利用者repositoryへ作成されたか

Template repositoryや別repositoryへ保存されている場合はrepository bindingを最優先で修正します。
