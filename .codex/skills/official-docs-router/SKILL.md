---
name: official-docs-router
description: 指定技術と関連技術を一次Sourceから固定点まで探索し、Inventory・Evidence・Version/Status・Coverageを反復監査してから、承認済み構成をOverview / Mechanism SkillへRoutingする。Research Directoryは「〜リサーチ」と命名し、既存の概要・仕組みNoteを勝手にResearchへ吸収しない。
---

# Official Docs Router

このSkillは`.codex/skills/official-docs-router/BASE.md`にあるDiscovery / Inventory / Evidence Consistency / Selection / Coverage / Structure / Human Approval / Routing / Final Rediscoveryの全ルールを維持し、日本語のInformation Architectureに関する追加ルールを定義します。

## 必ず読む基礎ルール

最初に必ず以下を全文読みます。

- `.codex/skills/official-docs-router/BASE.md`
- `.codex/skills/COMMON.md`
- `.codex/skills/MARKDOWN.md`
- `.codex/skills/overview-note/SKILL.md`
- `.codex/skills/overview-interrogate/SKILL.md`
- `.codex/skills/overview-review/SKILL.md`
- `.codex/skills/mechanism-note/SKILL.md`
- `.codex/skills/mechanism-interrogate/SKILL.md`
- `.codex/skills/mechanism-review/SKILL.md`
- `docs/authoring-workflow.md`

`BASE.md`のHuman Approval Gate、Pruning Default Keep、最低3 Discovery Round、Discovery Frontier、Name Collision / Lineage Audit、2回連続Discovery Closure、Global Reset、Recursive Semantic Inventory、Evidence Consistency、Coverage Contract、Selection Audit、Structure Audit、Proposal前Final Audit、Sub-skill Routing、Fresh Rediscovery、Completion条件はすべて必須です。

**命名とResearch Directoryの扱いについて`BASE.md`や`COMMON.md`と競合する場合は、このSKILLのルールを優先します。**


## Research Build Manifestと自動Recovery

`BASE.md`の承認済みTree Manifest、Checkpoint、Post-build Reconciliationは必須です。
構成承認後は`.codex/research-runs/<target>.json`を作り、各Directory / NoteをStage単位で追跡します。
途中停止したResearchは`python3 scripts/research-manifest.py resume <manifest>`で最初の未完了Itemを取得し、そのStageから冪等に再開します。

**「作成予定だったNoteを覚えているはず」と会話履歴へ依存してはいけません。**
**`python3 scripts/research-manifest.py validate <manifest>`が成功するまで「全Note作成済み」と宣言してはいけません。**

## Directory名だけを「〜リサーチ」にする

複数のDocumentation、Specification、Repository、Blog、Sampleなどを調査して再構成したDirectoryは、調査成果の集合だと分かるように命名します。

ルートDirectoryは原則として次の形式にします。

```text
<技術名>リサーチ
```

子Directoryも次の形式を基本にします。

```text
<技術名またはテーマ>リサーチ
```

良い例:

```text
AP2リサーチ
AP2 v0.2仕様リサーチ
AP2プロトコル連携リサーチ
AP2 SDK・実装リサーチ
AP2 Community Specification 2025.0リサーチ
AP2の進化・標準化リサーチ
AP2外部バインディングリサーチ
x402リサーチ
x402 v2仕様リサーチ
```

避ける例:

```text
AP2ドキュメントリサーチノート
AP2 v0.2仕様リサーチノート
AP2 公式・関連情報 日本語ノート
Canonical AP2 v0.2
プロトコル連携
SDKとリファレンス実装
```

**`リサーチ`を付けるのはDirectoryです。各NoteのTitleへ`リサーチノート`や`リサーチ`を機械的に付けてはいけません。**
Noteは、その記事で何を学ぶかが自然に分かる通常のTitleにします。

## 既存の概要・仕組みNoteをResearchへ吸収しない

Research Directoryを追加する時、既存のLearn記事を自動的にDirectory配下へ移動・改名・削除してはいけません。

特に既存の以下は独立した学習導線として扱います。

- `〜とは何か`などのOverview Note。
- `〜の仕組み`、`〜を技術的に理解する`などのMechanism Note。
- 実装・設計・運用を独立して説明する既存Note。

Research Sourceと内容が重複していても、既存Noteの`id`、`permalink`、カテゴリ上の配置を維持します。
Research Directory側で横断調査の入口が必要なら、**別ID・別PermalinkのResearch用Overview Noteを新規作成**します。

既存NoteをResearchへ移す、統合する、削除するのは、ユーザーがその変更を明示的に承認した場合だけです。

Structure Auditでは以下を必ず確認します。

```text
Existing Standalone Note Absorbed Without Approval = 0
Existing Standalone Note Deleted Without Approval = 0
Duplicate ID / Permalink = 0
```

## Note名は通常の記事名にする

Note名は固有名詞を保持しつつ、何を理解するNoteかが日本語で分かる名前へ再構成します。

公式Titleの逐語訳や、英語の正式名称へ`の仕組み`を付けただけの命名は避けます。
一方で、説明を詰め込みすぎた長いTitleにもしてはいけません。

良い例:

```text
AP2とは何か
AP2の仕組みを技術的に理解する
AP2 v0.2の全体構造と検証の分担
利用者の権限をAgentへ委任して検証する仕組み
利用者が同席する時・しない時の取引フロー
AP2が想定する攻撃とプライバシー対策
AP2・A2A・MCP・UCPは何を分担するのか
AP2とx402をどう組み合わせるのか
```

避ける例:

```text
Agent Authorization Frameworkの仕組み
Security and Privacy
Implementation Considerations
AP2公式仕様リサーチノート
AP2 x402リサーチノート
```

正式名称はFront Matterの`spec`、`official`、Source Metadata、本文初出で保持します。

## 本文見出しは短く自然な日本語にする

本文のH2/H3/H4は、英語見出しの直訳ではなく、目次として読んだ時に内容が分かる自然な日本語へします。

ただし長い説明文を見出しへ押し込む必要はありません。
見出しは「短いが意味がある」を優先します。

例:

```text
Manipulated Checkout
→ Checkout改ざんへの対策

Payment Credential Theft
→ Payment Credential盗難への対策

Runtime Architecture
→ 実装構成

Current Source
→ 現行Sourceを優先する
```

Protocol名、Role名、Field名など検索性に必要な識別子は原文を残して構いません。

## Information Architectureの追加ルール

`BASE.md`のInformation Architecture設計に加えて以下を必須にします。

- ResearchのルートDirectoryは原則`<技術名>リサーチ`。
- Researchの子Directoryは原則`〜リサーチ`。
- `リサーチノート`というSuffixをDirectoryにもNoteにも付けない。
- Note Titleは通常の記事名として自然な日本語にする。
- 既存Standalone Noteは承認なしにResearch Directoryへ移さない。
- Research用Overviewが必要なら既存Overviewを流用せず別Noteにする。
- `[Overview]` / `[Mechanism]`は内部Routing Labelなので維持する。

## Structure Auditの追加項目

`BASE.md`のStructure Auditに加え、以下を検査します。

- Root Research Directoryが`〜リサーチ`になっているか。
- Child Research Directoryが`〜リサーチ`になっているか。
- Directoryに`リサーチノート`が残っていないか。
- Noteに不要な`リサーチ` / `リサーチノート`Suffixが付いていないか。
- 既存Standalone Noteを勝手にResearchへ吸収していないか。
- Note名が日本語として自然か。
- H2/H3/H4に直訳調・英語だけの一般概念見出しが残っていないか。

完了条件へ以下を追加します。

```text
Directory Research Naming Missing = 0
Research Suffix On Note = 0
Existing Standalone Note Absorbed Without Approval = 0
Existing Standalone Note Deleted Without Approval = 0
Literal Translation Title = 0
Literal Translation Heading = 0
Meaningless English Heading = 0
```

## 構成提案の基本形

Research Directoryは次のように提案します。

```text
📁 <技術名>リサーチ
├─ <Research全体の読み方を整理するNote> [Overview]
├─ 📁 <テーマ>リサーチ
│  ├─ <通常の日本語Note名> [Mechanism]
│  └─ <通常の日本語Note名> [Mechanism]
└─ 📁 <関連Specification Family>リサーチ
   └─ <通常の日本語Note名> [Mechanism]
```

既存Overview / Mechanism Noteがある場合はResearch Treeの外に維持し、提案時にも別枠で明示します。

```text
カテゴリ直下の既存Note
├─ <技術名>とは何か
└─ <技術名>の仕組みを技術的に理解する

Research Directory
└─ 📁 <技術名>リサーチ
   └─ ...
```

## Human Approval Gate

`BASE.md`のHuman Approval Gateは引き続き必須です。
承認後の実装でも、既存Standalone NoteをResearchへ移す変更は承認範囲に含まれているか確認します。

## Completionへの追加条件

`BASE.md`のCompletion条件に加え、以下をすべて満たすまで完了扱いにしません。

- Directory Research Naming Missing = 0。
- Research Suffix On Note = 0。
- Existing Standalone Note Absorbed Without Approval = 0。
- Existing Standalone Note Deleted Without Approval = 0。
- Duplicate ID / Permalink = 0。
- Literal Translation Title = 0。
- Literal Translation Heading = 0。
- Meaningless English Heading = 0。
- 既存Standalone NoteのURLとIDを維持した。
- 全Research Directoryが`〜リサーチ`で終わる。
- Note表示Titleが通常の記事名として自然な日本語になっている。
- 全NoteのH2/H3/H4を再走査し、直訳調・英語だけの一般見出しが残っていない。
