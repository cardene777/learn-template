# Learn Deployer Troubleshooting

このReferenceは`learn-deployer`でDeploymentまたは編集E2Eが失敗した時だけ使用します。

`docs/setup.md`を人間向け手順のSource of Truthとして扱い、このファイルには失敗時の切り分けだけを置きます。

## まず確認するEvidence

推測で修正せず、利用可能なToolから次を取得します。

1. Failed Workflow Run ID。
2. Failed Job / Step名。
3. Failed Stepのログ末尾と最初の具体的なError。
4. 対象Commit SHA。
5. `wrangler.jsonc`のWorker名。
6. `src/index.js`のGitHub credential参照方法。
7. Deployment後ならWorker Version ID。

Secret値は取得・表示しません。

## Missing GitHub Actions Secret

代表例です。

```text
Missing GitHub secret: CLOUDFLARE_API_TOKEN
Missing GitHub secret: CLOUDFLARE_ACCOUNT_ID
```

対応です。

- GitHub repositoryのActions Secrets設定を確認する。
- Secret値をチャットへ貼らせない。
- 安全なSecret書き込みToolが無ければ、対象Secret名だけを示して本人に登録してもらう。
- 登録後はWorkflowを再実行して検証する。

## Worker GitHub credential未設定

代表例です。

```text
github_token_not_configured
```

または編集UIで本文読込が失敗し、Worker側がGitHub APIへ進めていないケースです。

確認します。

- GitHub Actionsで`WORKER_GITHUB_TOKEN`をCloudflareへ投入する構成か。
- 既存Cloudflare Secretを再利用する構成か。
- Workerが認識するSecret名。

Secret名のFallbackが実装されている場合は、現在コードで認識する名前を読んで判断します。過去の名前を記憶だけで決めないでください。

## GitHub API 401 / 403

原因候補です。

- Fine-grained PATの期限切れ。
- Repository accessの対象外。
- `Contents: Read and write`不足。
- Token所有者が対象repositoryへアクセスできない。

対応です。

- Token値ではなく、PATのRepository access / Permission / Expirationを本人に確認してもらう。
- 新しいTokenが必要なら本人が発行し、Secret UIへ直接登録する。
- 再登録後に編集APIまたはWorkflowで検証する。

## GitHub API 409 / source_changed_reload

本文編集中にGitHub側sourceが更新された可能性があります。

これはCredential障害として扱わないでください。

- 最新sourceを再読込する。
- ユーザー変更とのConflictを確認する。
- 古いSHAのまま強制上書きしない。

## Cloudflare authentication failure

確認します。

- `CLOUDFLARE_ACCOUNT_ID`が対象Accountか。
- API TokenがWorkersを編集できるか。
- Token scopeが対象Accountを含むか。
- Worker deploy logのCloudflare error code/message。

Accountが複数ある場合、推測で選択しません。

## Worker name conflict

`wrangler.jsonc`の`name`が既存Workerと衝突している、または別環境を上書きしそうな場合です。

- Cloudflare側を読めるToolがあれば既存Workerを確認する。
- 利用者専用名へ変更する。
- GitHub repository名とWorker名を同じにする必要はない。
- 名前変更後にDeploy URLを推測せず、Wrangler出力から取得する。

## Build validation failure

Metadata、Directory、Astro build、Source contractなどで失敗した場合です。

- Failed validation script名を特定する。
- ログの具体的なfile/pathを読む。
- Validationを無効化して通すのではなく、source contractを満たす修正を優先する。
- Templateの初期サンプルで失敗する場合は配布Templateのregressionとして扱う。

## Browser smoke failure

まずUI実装かTest固定値かを切り分けます。

- 特定ノート名・固定Route・個人データ依存がSmoke Testに残っていないか。
- desktop/mobileどちらで失敗したか。
- DOM欠落、overflow、visibility、click状態のどれか。

Template利用者の任意コンテンツで動く必要があるため、Testを特定private noteへ固定しないでください。

## Header GitHub linkが元Templateを指す

確認します。

- Header component内のrepository marker。
- `.github/workflows/deploy-cloudflare.yml`のrepository binding Step。
- build時の`${{ github.repository }}`。

利用者repositoryへ自動bindingする設計を維持します。

固定repository URLを利用者ごとに手修正する運用へ戻さないでください。

## 本文編集だけ失敗する

Site表示とBasic Authが成功していて、本文編集だけ失敗する場合です。

切り分け順です。

1. Worker GitHub credential設定。
2. GitHub PAT permission / expiration。
3. Workerが参照するrepository。
4. `/api/manage/body`のstatus/error code。
5. Source path / SHA conflict。

ブラウザへGitHub Token入力を復活させる修正はしないでください。

## Deploy成功後に表示が古い

- Deploy対象Commit SHAを確認する。
- Worker Version IDを確認する。
- Workflowが古いRunではないか確認する。
- Browser cacheだけの問題か、Cloudflare deployment propagationかを切り分ける。

新しいRunが成功していないのに「キャッシュです」と決めつけないでください。

## E2E保存後に再デプロイされない

確認します。

- Commit先branchが`main`か。
- Workflow `on.push.branches`。
- Workflow `paths`に変更ファイルが含まれるか。
- Commitが利用者repositoryに作成されたか。

保存先がTemplate repositoryや別repositoryなら最優先でrepository bindingを修正します。
