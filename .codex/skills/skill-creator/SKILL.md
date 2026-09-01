---
name: skill-creator
description: 新しいCodex/Agent Skillを作成・既存Skillを改善するためのSkill。ユーザーが「Skillを作りたい」「この手順をSkill化したい」「SKILL.mdを書きたい」「既存Skillを改善したい」「再利用可能なAIワークフローにしたい」と言った時は明示的な指定がなくても使用する。`.codex/skills/<skill-name>/SKILL.md`を中心に、トリガー設計、progressive disclosure、必要なreferences/scripts/assets、テストプロンプトまで設計する。
---

# Skill Creator

このSkillは、このrepositoryで再利用可能なSkillを作成・改善するための標準手順です。

Anthropicが公開しているAgent Skills / `skill-creator`の設計原則を参考にしていますが、このファイルは`__LEARN_REPOSITORY__`の`.codex/skills`運用に合わせて独自に整理したものです。

## ゴール

Skillを「長いプロンプト置き場」にしないでください。

良いSkillは次を満たします。

1. 何を実行するSkillかが明確である。
2. いつ読み込むべきかがfrontmatterの`description`だけで判断できる。
3. 実行手順と成功条件が明確である。
4. 必要な情報だけを段階的に読み込める。
5. repository固有の知識と一般知識を混同しない。
6. 同じ作業を別セッションでも再現できる。

## 配置

新しいSkillは原則として次へ置きます。

```text
.codex/skills/<skill-name>/
├── SKILL.md
├── references/     # 必要な時だけ
├── scripts/        # 決定的・反復的な処理がある時だけ
├── assets/         # 出力へコピーする素材がある時だけ
└── evals/          # 検証プロンプトを保存する時だけ
```

Skill本体以外のファイルを理由なく増やさないでください。

単純なSkillなら`SKILL.md`だけで十分です。

## 作成フロー

### 1. 既存Skillを確認する

新規作成前に`.codex/skills/`を確認してください。

同じ責務を持つSkillが既にある場合は、新規Skillを増やすより既存Skillの改善を優先します。

このrepositoryの文章生成・調査系Skillでは、必要に応じて次も確認します。

```text
.codex/skills/COMMON.md
.codex/skills/MARKDOWN.md
```

既存ルールと矛盾する指示を新しいSkillへ複製しないでください。

### 2. Intentを確定する

現在の会話や作業履歴から、まず次を抽出してください。

- Skillが可能にする作業。
- 使用すべきユーザー要求・文脈。
- 期待する成果物。
- 必須入力。
- 利用するTool・外部サービス。
- 成功条件。
- 失敗しやすいEdge Case。

会話から分かる情報を再質問しないでください。

不足情報だけを質問します。

### 3. Skill境界を決める

1つのSkillへ無関係な責務を詰め込まないでください。

次のどちらかなら分割を検討します。

- トリガー条件が大きく異なる。
- 成果物や検証方法が大きく異なる。
- Skill本文が長くなり、毎回ほとんど読まれない章が増える。

逆に、同じ作業の小さなVariationだけでSkillを乱立させないでください。

### 4. Frontmatterを書く

最低限`name`と`description`を定義します。

```yaml
---
name: example-skill
description: 何をするSkillか。どの要求・キーワード・文脈で使用するか。明示的にSkill名を指定されなくても、該当作業なら使うことが分かるように書く。
---
```

`description`はSkillの主要なTriggerです。

「いつ使うか」を本文だけに書かないでください。本文はSkillが選択された後に読むためです。

Trigger漏れを避けるため、次を含めます。

- 具体的な作業名。
- ユーザーが使いそうな言い換え。
- 関連する成果物名。
- 暗黙的に適用すべき文脈。

### 5. SKILL.md本文を書く

命令形で、実行順序が分かるように書きます。

ただし機械的に`MUST`を並べるのではなく、重要な制約には理由を添えてください。

本文には主に次を置きます。

- 目的。
- 実行フロー。
- 判断基準。
- Input / Output契約。
- Quality Gate。
- よくある失敗と回避方法。

一般論や巨大な参考資料は本文へ詰め込まず`references/`へ分離します。

### 6. Progressive Disclosureを使う

情報を3段階に分けます。

1. frontmatterの`name`と`description`。
2. Trigger後に読む`SKILL.md`本文。
3. 必要なケースだけ読む`references/`・実行する`scripts/`。

例えば複数Providerに対応するSkillなら次のようにします。

```text
cloud-deploy/
├── SKILL.md
└── references/
    ├── cloudflare.md
    ├── aws.md
    └── gcp.md
```

`SKILL.md`にはProvider選択ルールだけを書き、選択後に該当referenceを読みます。

### 7. scriptsを使う条件

次の処理は自然言語だけで毎回再実装せず、`scripts/`へ切り出すことを検討します。

- 同じファイル変換を何度も行う。
- Validationが決定的に書ける。
- 大量ファイルを機械的に検査する。
- 同じScaffoldを生成する。

Scriptは入力、出力、失敗条件を明確にしてください。

SkillがScriptを使う場合は、本文に「いつ、何のために実行するか」を書きます。

### 8. repository固有値を埋め込まない

再利用を想定するSkillでは、個人名、固定repository、固定URL、token、account IDを直接埋め込まないでください。

必要なら環境変数・入力値・repository metadataから取得します。

SecretはSkill本文・examples・evalsへ書かないでください。

### 9. Output契約を明確にする

成果物に決まった形式がある場合はテンプレートを定義します。

例です。

```markdown
## Output

# Title

## Summary

## Findings

## Recommendation
```

厳密な形式が不要なSkillでは、不要なフォーマット制約を追加しないでください。

### 10. テストプロンプトを作る

客観的に検証しやすいSkillでは、実際にユーザーが言いそうな2〜3個のプロンプトを作ります。

少なくとも次を混ぜます。

- 典型ケース。
- Triggerが曖昧なケース。
- Edge Caseまたは失敗しやすいケース。

必要なら`evals/evals.json`へ保存します。

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "ユーザーの実際の依頼に近い文",
      "expected_output": "成功時に満たすべき結果",
      "files": []
    }
  ]
}
```

単純な文章スタイルSkillなど、定量評価の意味が薄い場合は過剰なeval環境を作らないでください。

### 11. Quality Gate

作成後に次を確認します。

- `name`とdirectory名が一致している。
- `description`だけでTrigger条件が分かる。
- Skill本文に「いつ使うか」だけを依存させていない。
- 既存Skillと責務が重複していない。
- Secretや個人情報が含まれていない。
- 固定repositoryや固定accountへ依存していない。
- 必要なreferenceが本文から明示的に参照されている。
- 不要なREADMEや説明ファイルを増やしていない。
- 実行可能Scriptには失敗条件がある。
- 成果物の成功条件を説明できる。

## 既存Skillを改善する時

既存Skillの`name`は原則変更しません。

まず「何が失敗したか」を特定し、必要最小限の修正を行います。

よくある改善箇所です。

- Triggerされない → `description`へユーザー表現・関連文脈を追加する。
- Triggerされすぎる → 対象外条件を明確にする。
- 出力が不安定 → Output契約・判断基準・Quality Gateを追加する。
- 本文が長すぎる → referenceへ分離する。
- 毎回同じコードを書く → scriptへ切り出す。
- repository固有値が混ざる → 入力・環境変数へ置き換える。

## このrepository用テンプレート

新規Skillを作る時は必要に応じて次を参照してください。

```text
.codex/skills/skill-creator/references/skill-template.md
```

テンプレートを全項目埋めること自体を目的にしないでください。

Skillの責務に不要な節は削除します。

## 参考設計

このSkillの設計時にはAnthropicの公開`anthropics/skills`にある`skill-creator`を参考にしています。

特に次の考え方を採用しています。

- `description`を主要Triggerとして扱う。
- `SKILL.md`とbundled resourcesを分離する。
- Progressive disclosureでContext量を抑える。
- 実際のユーザープロンプトでSkillを検証する。

公式実装は変化する可能性があるため、Anthropic互換性が重要な変更を行う時は最新の一次情報を確認してください。
