# Skill Template

必要な節だけ残して使ってください。

```markdown
---
name: your-skill-name
description: このSkillが何を行い、どのユーザー要求・言い換え・文脈で使用するかを書く。明示的にSkill名を指定されなくても該当作業なら使うことが分かるようにする。
---

# Your Skill Title

このSkillの目的を短く説明します。

## Goal

成功状態を説明します。

## Inputs

必要な入力だけを書きます。

## Workflow

1. 最初に確認すること。
2. 調査・判断すること。
3. 成果物を作ること。
4. Validationすること。

## Decision rules

迷いやすい分岐条件を書きます。

## Output

必要な場合だけ成果物形式を定義します。

## Quality Gate

- 成功条件1。
- 成功条件2。
- 禁止事項またはよくある失敗。

## References

必要なreferenceだけを、いつ読むかと一緒に列挙します。
```

## Frontmatter checklist

- directory名と`name`を一致させる。
- `description`へ「何をするか」と「いつ使うか」の両方を書く。
- ユーザーが実際に使いそうな言い換えを含める。
- Trigger情報を本文だけへ置かない。

## Resource checklist

`references/`は長い仕様・Provider別情報・詳細な例を分離する時に使います。

`scripts/`は決定的・反復的な処理を自動化する時に使います。

`assets/`は成果物へコピーするテンプレートや素材がある時だけ使います。

`evals/`は客観的に検証できるSkillのテストプロンプトを保存する時に使います。

空のdirectoryを先回りして作る必要はありません。
