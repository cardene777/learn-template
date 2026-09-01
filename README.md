# Learn Template

GitHub上のMarkdownをSource of Truthとして管理し、Astroで生成してCloudflare Workersへデプロイする個人用ナレッジベースTemplateです。

## Setup

セットアップ手順は[docs/setup.md](docs/setup.md)だけを見れば完了できます。

GitHubの`Use this template`から自分のrepositoryを作成した後、ChatGPTへrepository URLと一緒に次のように依頼できます。

```text
このGitHub repositoryを使ってください:
https://github.com/<YOUR_NAME>/<YOUR_REPOSITORY>

repository内の .codex/skills/learn-deployer/SKILL.md を使って、
このLearnを自分用にセットアップしてCloudflareへデプロイまで進めて。
```

Secret値は通常のチャットへ貼らないでください。`learn-deployer`は現在状態を確認し、Toolで実行できる作業は自動実行し、本人操作が必要な箇所だけを案内します。

## Default

- Basic Auth: 有効にして使う
- ブラウザ編集: 任意。使わない場合はGitHub PAT不要
- デプロイ: GitHub Actions → Cloudflare Workers

`contents/`には表示確認用の中立なサンプルだけが入っています。自分のノートを追加した後は削除して構いません。

## Skills

Public Templateに含めるSkillは2つだけです。

- [Learn Deployer](.codex/skills/learn-deployer/SKILL.md): セットアップ、Cloudflareデプロイ、失敗復旧
- [Skill Creator](.codex/skills/skill-creator/SKILL.md): このrepository用の新しいSkillを作成・改善
