# Learn Template

GitHub上のMarkdownをSource of Truthとして管理し、Astroで生成してCloudflare Workersへデプロイする個人用ナレッジベースTemplateです。

## 動作サンプル

https://learn-template-test.cardene777.workers.dev/

## 最短セットアップ

初回デプロイは**WranglerからCloudflareへ直接デプロイ**するのが最短です。

1. `Use this template`で自分のrepositoryを作る。
2. Cloudflareアカウントを用意する。
3. WranglerでCloudflareへログインする。
4. Basic Auth Secretを安全に用意する。
5. `npm run deploy:cloudflare`でデプロイする。

GitHub Actions用のCloudflare API Tokenは、初回の直接デプロイでは不要です。

詳しい手順は[docs/setup.md](docs/setup.md)にまとめています。

## ChatGPTからセットアップする

セットアップ専用Skillは[Learn Deployer](.codex/skills/learn-deployer/SKILL.md)です。

このTemplateでは、**ChatGPTデスクトップアプリから実行することを推奨**します。GitHubやCloudflareのPlugin / Connector、Wranglerを利用できる環境を優先して、ChatGPTにできる操作はそのまま実行させます。

デプロイを始める前に、ChatGPTで次の連携を準備してください。

1. GitHub Plugin / Connectorを追加して、対象repositoryへアクセスできる状態にする。
2. Cloudflare Plugin / Connectorが利用可能な環境では追加して、Cloudflareアカウントへ接続する。
3. Cloudflare Plugin / ConnectorがChatGPT内で見つからない場合は、そのまま進める。`learn-deployer`がWrangler OAuth / device loginへfallbackする。

チャット内からPlugin追加UIを表示できる環境では、`learn-deployer`がGitHubとCloudflareを検索し、未接続の連携をチャット内で追加できるよう案内します。ChatGPT内で追加できない場合だけ、Plugin一覧から手動で追加します。

GitHub repository URLと一緒に次のように依頼できます。

```text
このGitHub repositoryを使ってください:
https://github.com/<YOUR_NAME>/<YOUR_REPOSITORY>

https://github.com/cardene777/learn-template
上記のテンプレートrepository内の `.codex/skills/learn-deployer/SKILL.md` を使って、
ChatGPT Desktop / Pluginの準備確認から始めて、Cloudflareへデプロイして。
```

Cloudflareアカウントが無ければ、`learn-deployer`がデプロイ前にアカウント作成手順を表示します。Wranglerのdevice loginが使える環境では、API Tokenを発行せずOAuth認証で進めます。

Secret値は通常のチャットへ貼らないでください。

## ChatGPTからノートを作成する

ノート作成用Skillは[Overview Note](.codex/skills/overview-note/SKILL.md)と[Mechanism Note](.codex/skills/mechanism-note/SKILL.md)です。

通常はSkill名を指定する必要はありません。各Skillの`description`に書かれたTriggerから、依頼内容に合うSkillを自動選択します。

ノートの配置、frontmatter、検証、repositoryへのCommitはSkill側に任せるため、利用者は**このチャットで何をノートに残したいか**だけを伝えます。

最初に対象repositoryだけ指定します。

```text
このGitHub repositoryを使ってください:
https://github.com/<YOUR_NAME>/<YOUR_REPOSITORY>
```

### 概要ノートを作る

会話で話したテーマの全体像、目的、主要な概念を整理したい場合は、次のように依頼します。

```text
この会話で話した「〇〇」について概要ノートにまとめてください。
```

会話全体を対象にする場合は、さらに短くできます。

```text
この会話で話した内容を概要ノートにまとめてください。
```

この依頼は`overview-note`が対象です。

### 仕組みノートを作る

会話で話したテーマの内部構造、処理フロー、コンポーネント同士の関係を整理したい場合は、次のように依頼します。

```text
この会話で話した「〇〇」の仕組みをノートにまとめてください。
```

この依頼は`mechanism-note`が対象です。

### 概要ノートと仕組みノートを両方作る

同じテーマについて全体像と内部構造を分けて残したい場合は、次のように依頼します。

```text
この会話で話した「〇〇」について、
概要ノートと仕組みノートをそれぞれ作ってください。
```

この場合は`overview-note`と`mechanism-note`を併用します。

### Skillを明示して呼び出す

Skillを明示したい場合だけ、実際のSkill名を指定します。

```text
overview-note Skillを使って、この会話で話した「〇〇」についてまとめてください。
```

```text
mechanism-note Skillを使って、この会話で話した「〇〇」の仕組みについてまとめてください。
```

参考URLや追加資料がある場合だけ、これらの依頼文の後ろへ追加します。

## Default

- Basic Auth: ON
- ブラウザ編集: OFF。必要な場合だけGitHub PATを追加
- 初回デプロイ: Wrangler direct deploy
- 自動デプロイ: 必要な場合だけGitHub ActionsまたはCloudflare Git integration

`contents/`には表示確認用の中立なサンプルだけが入っています。自分のノートを追加した後は削除して構いません。

## Skills

Public Templateに含めるSkillは4つです。

- [Learn Deployer](.codex/skills/learn-deployer/SKILL.md): ChatGPT Desktop / Plugin準備、Cloudflare準備、直接デプロイ、自動デプロイ、失敗復旧
- [Overview Note](.codex/skills/overview-note/SKILL.md): 会話内容から全体像、目的、主要概念を概要ノートとして保存
- [Mechanism Note](.codex/skills/mechanism-note/SKILL.md): 会話内容から内部構造、処理フロー、コンポーネント関係を仕組みノートとして保存
- [Skill Creator](.codex/skills/skill-creator/SKILL.md): このrepository用の新しいSkillを作成・改善
