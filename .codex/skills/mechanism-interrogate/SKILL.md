---
name: mechanism-interrogate
description: 概要ノートを土台にした仕組みノートを、クライアント・実装者・Security・障害解析・仕様厳密性の視点から破壊テストし、深い技術質問へ答えられるまでGapを収束させる。
---

# Mechanism Interrogate

このSkillはFAQ生成ではありません。
仕組みノートが、概要ノートから自然につながり、クライアントや実装者の深い技術質問へ記事だけで答えられるかを破壊テストします。

## 事前確認

最初に次を読みます。

- `.codex/skills/COMMON.md`
- `.codex/skills/MARKDOWN.md`
- `.codex/skills/mechanism-note/SKILL.md`
- `.codex/skills/mechanism-review/SKILL.md`
- 対象技術の完成済み概要ノート
- 対象仕組みDraft全文
- 対象Versionの公式Specification、Architecture、Schema、Security、Flow、Error、必要ならReference Implementation
- 実際のクライアント質問、過去Q&A、レビュー指摘

概要ノートが存在する場合、それを読まずにInterrogationを開始してはいけません。

## 必須作業物

### 1. Overview → Mechanism Traceability Matrix

概要ノートの主要理解ポイントごとに、仕組みノートでどの技術詳細へ展開したかを確認します。

重要なOverview Pointが仕組み側で消えていればMajorです。

### 2. Official Mechanism Coverage Matrix

公式仕様の主要Data、Flow、Architecture、State、Validation、Security、Failure、Implementation Boundaryを意味単位へ分解します。

重要Mechanismは、記事だけで`入力 → 誰が処理 → 何を検証 → どう判断 → 何が変わる → なぜ必要 → 失敗時`を追える場合だけCoveredです。

### 3. Client Question Coverage Matrix

クライアントや実装者が持つ質問を次のCategoryで整理します。

- Data
- Flow
- Architecture
- Security
- State
- Failure
- Implementation
- Integration
- Scope / Version

実際の質問がない場合は、概要ノートの各Sectionから「次に技術者が聞く質問」を導出します。

Critical / Majorな質問に記事だけで答えられなければ完了しません。

## Persona

### クライアント技術担当

- 結局どんなDataを送るのか。
- どのSystem間で通信するのか。
- 既存Systemのどこに入れるのか。
- どのComponentを新しく作る必要があるのか。
- どの責任を既存Providerへ任せられるのか。
- PoCでは最低限どこまで必要か。

### 初めて実装する技術者

- 最初に何を受け取るのか。
- 誰がDataを作るのか。
- 必須Fieldは何か。
- そのFieldは次のどの処理で使うのか。
- RequestとResponseをどう対応付けるのか。

### Backend Engineer

- 何を保存する必要があるか。
- Transaction Boundaryはどこか。
- 同じRequestが重複したらどうなるか。
- 並行実行で二重処理できないか。
- 外部Service失敗時にどのStateが残るか。

### Architecture Reviewer

- Roleと実装Componentはどう対応するか。
- Client / Backend / Agent / Verifier / Store / External Providerはどう分かれるか。
- SecretやSigning Keyはどこに置くか。
- Trust Boundaryはどこか。
- 検証を迂回してSide Effectへ到達できないか。

### Security Engineer

- 誰が何を署名するか。
- 何と何を結び付けているか。
- 差し替え、Replay、別Transactionへの流用はできないか。
- 暗号学的な検証と権限判断を混同していないか。
- SignatureがValidでもRejectされる条件は何か。

### 障害解析担当

- どの段階で失敗したか判別できるか。
- 失敗時にどのDataが残るか。
- 何を再検証すれば原因を切り分けられるか。
- Receipt、Log、Stateは何を示すか。

### 仕様厳密性

- MUST / SHOULD / MAYのどれか。
- Version固有か。
- Schema上必須かOptionalか。
- Sampleを仕様として断定していないか。
- Scope外をProtocol機能として書いていないか。

### 日本語読者

- 英語を知らなくても主要な因果関係を追えるか。
- 見出し、Table、Mermaidも日本語で意味が分かるか。

## Question Chain

概要ノートの重要Conceptごとに、次のように掘ります。

`概要では何か → 実際のDataは何か → 誰が作るか → どこへ送るか → 何を検証するか → 何を保存するか → どのComponentが担当するか → どこで許可・拒否するか → 失敗時どうなるか → 実装では何を作るか`

重要なConceptでは単発質問で終わらせません。

## Data Flow破壊テスト

主要Dataについて、次を全部答えられるか確認します。

- 生成者。
- Schema / Field。
- 送信先。
- 検証者。
- 判断への利用。
- 保存先。
- 次の利用。

どこかが切れていればMajorです。

## Architecture破壊テスト

主要Roleについて、実装Componentへ降りているか確認します。

- どのProcess / Serviceになるか。
- 何を入力にするか。
- 何を返すか。
- 何を保存するか。
- どのSecretを持つか。
- どの外部Serviceへ接続するか。
- どこで拒否できるか。

概要のRole説明をそのまま再掲しているだけならMajorです。

## Overview整合性破壊テスト

概要と仕組みを並べ、次を確認します。

- 同じConceptの意味が一致しているか。
- Flow順序が一致しているか。
- 仕組み側で新しい保証を勝手に追加していないか。
- 仕組み側で分かった重要な制約が概要に欠けていないか。

矛盾があればどちらかを修正します。

## Visual破壊テスト

複数主体の通信、Data Binding、状態遷移、検証分岐、Architecture、Trust Boundaryなどが複雑なのに文章だけで残っていればMajorです。

## Severity

### Critical

事実誤認、Security上危険な説明、主要Mechanism破綻、概要との重大矛盾、誤った実処理です。

### Major

- Overviewの重要ポイントが技術展開されていない。
- 主要クライアント質問へ答えられない。
- Data Flowが途中で切れている。
- ArchitectureがRole説明止まり。
- 実装責任が判断できない。
- 重要Coverage Missing。
- 日本語可読性やVisual Coverageが不足している。

### Minor

中心理解を壊さない局所的な不足です。

## Loop

1. Overview → Mechanism Traceability Matrixを作る。
2. Official Mechanism Coverage Matrixを作る。
3. Client Question Coverage Matrixを作る。
4. Data Flow Map、Architecture Map、Invariant / Boundary Map、Visual Planを確認する。
5. Personaごとに全文をInterrogateする。
6. Critical / MajorとPartial / Missingを集約する。
7. 概要ノートまたは一次情報へ戻って修正する。
8. 修正後全文を再Interrogateする。
9. 全Matrixを更新する。
10. 新しい説明から二次・三次質問を導出する。
11. Critical / Majorと重要なPartial / Missingが0になるまで繰り返す。

## Reviewとの相互Loop

Interrogation収束後に`mechanism-review`を実行します。
Review修正後は全Matrixを更新し、全文を再Interrogateします。

## No-change Final Round

完成前に本文を変更せずに済む最終Roundを1回通します。

## Completion

以下をすべて満たした時だけ完了です。

- OverviewとのCritical / Majorな対応漏れが0
- Official Mechanism CoverageのCritical / MajorにPartial / Missingが0
- Client Question CoverageのCritical / MajorにPartial / Missingが0
- 主要Dataを生成から利用まで追える
- 主要Architectureを実装Component単位で説明できる
- 日本語だけでも主要な処理と理由を説明できる
- 複雑な関係が適切に可視化されている
- Overviewとの矛盾がない
- Interrogation Critical = 0
- Interrogation Major = 0
- Review Critical = 0
- Review Major = 0
- 必要な再Interrogation / 再Reviewが完了
- 変更なし最終Roundを通過
