# Learn Template セットアップ

このドキュメントは、Templateから自分のLearnを作り、Basic Auth付きでCloudflare Workersへデプロイするための手順です。

## 最短ルート

おすすめは**WranglerからCloudflareへ直接デプロイ**です。GitHub Actions用のCloudflare API Tokenを最初から用意する必要はありません。

```text
Use this template
↓
Cloudflareアカウント確認 / 作成
↓
Wrangler login
↓
Basic Auth Secretを安全に用意
↓
npm run deploy:cloudflare
↓
workers.dev
```

ブラウザ編集を使わない場合、GitHub PATは不要です。

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
Cloudflareアカウントの準備確認から始めて、使えるならWranglerで直接デプロイして。
```

`learn-deployer`は最初にCloudflareの準備状況を確認します。アカウントが無ければ、先にアカウント作成手順だけを表示します。

Secret値は通常のチャットへ貼らないでください。

## 1. Templateからrepositoryを作る

Public Template repositoryで`Use this template`→`Create a new repository`を選びます。

ノートを非公開にしたい場合はPrivate repositoryを推奨します。

## 2. Cloudflareアカウントを準備する

Cloudflareアカウントを持っていない場合は、先にCloudflareでアカウントを作成し、必要ならメール認証を完了してください。

ChatGPTから進めている場合は、作成後に次だけ返せば十分です。

```text
作った
```

CloudflareのPasswordや認証情報をチャットへ送らないでください。

## 3. WranglerでCloudflareへログインする

Wranglerが使える環境では認証状態を確認できます。

```bash
npx --yes wrangler@4.127.1 whoami
```

未認証ならdevice loginを使います。

```bash
npx --yes wrangler@4.127.1 login --device
```

表示されたCloudflareの認証画面を開き、コードを承認します。

`--device`が使えない環境では通常のOAuth loginを使います。

```bash
npx --yes wrangler@4.127.1 login
```

この経路ではGitHub Actions用の`CLOUDFLARE_ACCOUNT_ID`と`CLOUDFLARE_API_TOKEN`は不要です。

## 4. Basic Authを用意する

Basic Authは標準で有効にします。

Worker Secret名は次です。

```text
BASIC_USER
BASIC_PASSWORD
```

Passwordはチャットへ貼らないでください。

Cloudflare Secretを安全に書き込めるToolがある場合はそれを使います。無い場合は、ローカルでgitignore済みのSecret fileを作れます。

例として`learn.secrets.json`を作り、値は自分の端末や安全な入力UIで直接入れます。

```json
{
  "BASIC_USER": "<username>",
  "BASIC_PASSWORD": "<password>"
}
```

`*.secrets.json`は`.gitignore`対象です。このファイルをCommitしないでください。

## 5. ブラウザ編集を使う場合だけGitHub PATを追加する

本文編集・タイトル編集からGitHubへCommitしたい場合だけFine-grained PATを作ります。

Repository accessは自分のLearn repositoryだけに限定し、最低限`Contents: Read and write`を付けます。

Secret file方式なら次のように追加します。

```json
{
  "BASIC_USER": "<username>",
  "BASIC_PASSWORD": "<password>",
  "GITHUB_TOKEN": "<fine-grained PAT>"
}
```

PAT値をチャットへ送らないでください。

## 6. Worker名を確認する

既定Worker名は`learn`です。

既存Workerを上書きしたくない場合は、Sourceを書き換えずに一時的なWorker名を指定できます。

```bash
LEARN_WORKER_NAME=my-learn npm run deploy:cloudflare
```

## 7. 直接デプロイする

依存関係を入れます。

```bash
npm install
```

通常はGitHub repositoryを`git remote origin`から自動判定します。

Secret fileを使う場合:

```bash
LEARN_SECRETS_FILE=./learn.secrets.json npm run deploy:cloudflare
```

Worker名も指定する場合:

```bash
LEARN_WORKER_NAME=my-learn \
LEARN_SECRETS_FILE=./learn.secrets.json \
npm run deploy:cloudflare
```

repositoryを自動判定できない環境では明示できます。

```bash
LEARN_REPOSITORY=<YOUR_NAME>/<YOUR_REPOSITORY> \
LEARN_SECRETS_FILE=./learn.secrets.json \
npm run deploy:cloudflare
```

`deploy:cloudflare`は次を行います。

1. GitHub repositoryを判定する。
2. repository bindingをデプロイ中だけ一時適用する。
3. 必要ならWorker名を一時変更する。
4. Astroをbuildする。
5. WranglerでCloudflare Workersへdeployする。
6. デプロイ後にSourceを元へ戻す。

Wranglerが表示したworkers.dev URLを使ってください。URLは推測しません。

## 8. 動作確認

最低限次を確認します。

- workers.devまたはCustom Domainへアクセスできる。
- Basic Authが有効。
- 正しいCredentialでページが表示される。
- ヘッダーのGitHubリンクが自分のrepositoryを指す。

編集を有効にした場合だけ追加で確認します。

- `本文編集`でMarkdownを読み込める。
- 保存すると自分のrepositoryへCommitされる。

## GitHub Actionsで自動デプロイしたい場合

pushごとに自動デプロイしたい場合は、同梱の`Astro Cloudflare Deploy`を使えます。

この経路ではGitHub Actions Secretsとして次が必要です。

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

Secret値はGitHubのSecret入力UIへ直接登録してください。

**初回デプロイだけならWrangler直デプロイの方が設定項目が少ないため推奨です。**

## ローカル開発

```bash
npm install
npm run dev
```

`.env`、`.dev.vars`、`*.secrets.json`、TokenやPasswordを含むローカルファイルはCommitしないでください。

## 問題が起きた場合

ChatGPTへrepository URLを渡し、次のように依頼できます。

```text
learn-deployerを使って現在のCloudflare認証・Worker・repository状態を確認し、失敗したところから直して。
```

最初の手順を繰り返さず、現在の未完了Gateから再開します。
