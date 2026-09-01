# Learn Template

GitHub上のMarkdownをSource of Truthとして管理し、Astroで静的HTMLを生成し、Cloudflare Workersで閲覧・編集できる個人用ナレッジベースのテンプレートです。

このrepositoryは配布用Template repositoryとして使うことを想定しています。

## Setup

セットアップ、GitHub/CloudflareのSecret設定、デプロイ、編集確認、Skillの使い方はすべて次のドキュメントにまとめています。

- [セットアップガイド](docs/setup.md)

GitHubの`Use this template`から自分専用repositoryを作成した後、上記手順に従ってください。

### ChatGPTからセットアップする

セットアップ専用Skillは[Learn Deployer Skill](.codex/skills/learn-deployer/SKILL.md)です。

ChatGPTへ依頼する時は、**GitHubで今開いている自分のrepository URLをコピーして一緒に渡してください**。Templateから作成した後のURLは次の形式です。

```text
https://github.com/<YOUR_NAME>/<YOUR_REPOSITORY>
```

例えば次のように依頼します。

```text
このGitHub repositoryを使ってください:
https://github.com/<YOUR_NAME>/<YOUR_REPOSITORY>

repository内の .codex/skills/learn-deployer/SKILL.md を使って、
このLearnを自分用にセットアップしてCloudflareへデプロイまで進めて。
```

すでに途中まで設定済みなら、現在の状態から再開できます。

```text
このGitHub repositoryの現在の状態を確認してください:
https://github.com/<YOUR_NAME>/<YOUR_REPOSITORY>

learn-deployerを使って、セットアップの続きを進めて。
```

デプロイ失敗の復旧にも使えます。

```text
このGitHub repositoryのCloudflareデプロイが失敗している:
https://github.com/<YOUR_NAME>/<YOUR_REPOSITORY>

learn-deployerを使って原因を確認し、続きから直して。
```

`learn-deployer`は現在のGitHub / Cloudflare / GitHub Actions状態を確認し、Toolで実行できる作業は自動実行します。Token発行やSecret入力など本人操作が必要な箇所だけをCheckpointとして案内し、その後のデプロイと編集E2E確認まで再開します。

GitHub PAT、Cloudflare API Token、Basic AuthのパスワードなどのSecret値は通常のチャットへ貼らないでください。

## Content

`contents/`には動作確認用の最小サンプルだけが入っています。

自分のノートを追加した後はサンプルを削除して構いません。

## Skills

`.codex/skills/`にはノート作成、Skill作成、Learn環境のセットアップを支援するSkillが含まれます。

セットアップ・デプロイには[Learn Deployer Skill](.codex/skills/learn-deployer/SKILL.md)を使います。

新しいSkillを作る時は[Skill Creator](.codex/skills/skill-creator/SKILL.md)を起点にしてください。
