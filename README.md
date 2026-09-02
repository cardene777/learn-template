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

GitHub repository URLと一緒に次のように依頼できます。

```text
このGitHub repositoryを使ってください:
https://github.com/<YOUR_NAME>/<YOUR_REPOSITORY>

https://github.com/cardene777/learn-template
上記のテンプレートrepository内の `.codex/skills/learn-deployer/SKILL.md` を使って、
Cloudflareアカウントの準備確認から始めて、使えるならWranglerで直接デプロイして。
```

Cloudflareアカウントが無ければ、`learn-deployer`がデプロイ前にアカウント作成手順を表示します。Wranglerのdevice loginが使える環境では、API Tokenを発行せずOAuth認証で進めます。

Secret値は通常のチャットへ貼らないでください。

## Default

- Basic Auth: ON
- ブラウザ編集: OFF。必要な場合だけGitHub PATを追加
- 初回デプロイ: Wrangler direct deploy
- 自動デプロイ: 必要な場合だけGitHub ActionsまたはCloudflare Git integration

`contents/`には表示確認用の中立なサンプルだけが入っています。自分のノートを追加した後は削除して構いません。

## Skills

Public Templateに含めるSkillは2つだけです。

- [Learn Deployer](.codex/skills/learn-deployer/SKILL.md): Cloudflare準備、直接デプロイ、自動デプロイ、失敗復旧
- [Skill Creator](.codex/skills/skill-creator/SKILL.md): このrepository用の新しいSkillを作成・改善
