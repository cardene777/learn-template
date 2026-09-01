---
name: mechanism-note
description: 完成済みの概要ノートを土台に、各概念をデータ、通信、検証、状態、アーキテクチャ、実装、失敗まで技術的に深掘りし、補足が必要な用語をMarkdownトグルで説明し、クライアントの深い質問へ答えられる仕組みノートを作成する。
---

# Mechanism Note

仕組みノートは概要ノートと別の世界を作る記事ではありません。
**概要ノートで作った全体理解を、そのまま技術レベルへ降ろす記事**です。

読者が概要ノートで「何か、なぜ必要か、誰が関わるか、全体としてどう動くか」を理解した後、仕組みノートでは「実際にどんなデータをやり取りし、どこで何を検証し、どの状態を持ち、どう実装するのか」まで説明できる状態を作ります。

最終目標は、クライアントや実装者から対象技術について深く質問された時に、記事を根拠として技術的に説明できることです。

## 最優先ルール

最初に以下を読みます。

- `.codex/skills/COMMON.md`
- `.codex/skills/MARKDOWN.md`
- 対象技術の完成済み概要ノート

対象技術に概要ノートが存在する場合、**仕組みノートは必ず概要ノートを基準に開始します。**
概要ノートを読まずに一次仕様だけから独立した構成を作ってはいけません。

概要ノートに誤りや不足を見つけた場合は、仕組みノート側だけで矛盾を隠さず、概要ノート側の修正候補として記録します。

日本語ノートでは、説明の主語・述語・因果関係を日本語で書きます。
英語は正式名称、Protocol名、Role名、API名、Field名、Claim名、Schema名など仕様との照合に必要なものへ限定します。

## 最優先ルール: 補足が必要な技術用語はトグルで閉じる

初学者または初めて実装する技術者が、本文を止めて外部検索しないと意味を確定できない用語は、`.codex/skills/MARKDOWN.md`の「用語補足トグル」に従って初出付近へ`<details>`を置きます。

仕組みノートでは特に次を重点対象にします。

- 略語、Protocol / Standard / Extension名。
- Role / Component / Evidence / Credential / Proof / Receiptなど仕様固有Concept。
- Field / Claim / Header / Identifierで、後続処理を理解するため意味が必要なもの。
- Signature、Hash、Canonicalization、Binding、Delegation、Nonce、Replay、IdempotencyなどSecurity / Protocol用語。
- State、Transition、Retry、Settlement、Authorizationなど、一般語と仕様上の意味がずれるもの。
- Draft / Candidate / Final等のStatus、Version固有用語。

本文にはその語がこのMechanismで何をするかを残し、トグルには正式名称、平易な定義、なぜ登場するか、何と混同しやすいか、保証範囲、短い例などを補足します。

MUST / SHOULD / MAY、検証条件、拒否条件、Security Boundary、実装責務をトグルだけへ隠してはいけません。

## 1. 概要ノートから理解の骨格を抽出する

最初に概要ノートを全文読み、主要な理解ポイントを抽出します。

例えば次です。

- 解決する問題。
- Role / Actor。
- 主要Concept。
- 主要Data。
- 全体Flow。
- 権限や信頼の境界。
- Verification。
- Failure / Scope外。
- 他技術との接続。
- 実装責務。

この時点では新しい記事構成を考えません。
まず「概要で何を理解したことになっているか」を固定します。

## 2. Overview → Mechanism Traceability Matrixを作る

概要ノートの主要理解ポイントを、仕組みノートでどこまで技術的に掘る必要があるかへ変換します。

最低限次を持ちます。

| 項目 | 内容 |
|---|---|
| Overview Location | 概要ノートのSection |
| Overview Point | 概要で説明している理解ポイント |
| Technical Questions | そこから生じる技術的な疑問 |
| Required Depth | Data / Flow / Architecture / State / Verification / Security / Failure / Implementationなど |
| Mechanism Location | 仕組みノートの対応Section |
| Status | Covered / Partial / Missing / Intentionally Not Expanded |
| Reason | 判定理由 |

重要なOverview Pointを理由なく仕組みノートから消してはいけません。
仕組みノートは概要ノートの技術的な続編であり、対応関係を追跡可能にします。

## 3. クライアント質問を先に設計する

概要ノートの各理解ポイントから、クライアント、設計者、実装者が次に聞きそうな質問を導出します。

例えば次です。

### データ

- 実際にどんなPayloadを送るのか。
- 必須Fieldは何か。
- そのFieldは誰が生成するのか。
- どのField同士が同じTransactionを結び付けるのか。
- 署名対象はどのByte列か。

### 通信と処理順

- どのComponent間で通信するのか。
- Request / Responseはどの順で進むのか。
- 同期処理か非同期処理か。
- 前のResponseのどの値を次のRequestへ使うのか。

### アーキテクチャ

- どのComponentが必要か。
- Client、Backend、Provider、外部Serviceの責任はどう分けるか。
- LLMと決定的なCodeはどこで分けるか。
- Trust Boundaryはどこか。

### 検証とSecurity

- 誰が誰の署名を検証するのか。
- 何をHashで結び付けるのか。
- 差し替え、Replay、二重利用はどこで止めるのか。
- SignatureがValidでも拒否されるのはどんな時か。

### State

- 何を保存する必要があるか。
- 状態はどの条件で変わるか。
- RetryやConcurrent Requestで何が起きるか。

### 実装

- 最低限どのModule / API / Storeを作る必要があるか。
- 既存Systemのどこへ組み込むか。
- どこまでProtocolが決め、どこからApplication実装か。
- PoCならどこまで作れば成立するか。

### 障害・運用

- どこで失敗するか。
- 失敗時に何が残るか。
- 再試行できるか。
- 後から何を見れば原因を追えるか。

これらを**Client Question Coverage Matrix**として管理します。
実際のクライアント質問や過去Q&Aがあれば最優先で追加します。

## 4. 一次情報で技術詳細を調査する

概要ノートを土台にした上で、仕組みノートに必要な深さを一次情報から追加調査します。

必要に応じて次を確認します。

- Specification / Architecture
- Protocol Flow
- API / Message
- Schema / Field
- State Machine
- Validation Rule
- Signature / Binding
- Security Consideration
- Error / Failure
- Implementation Guide
- Reference Implementation
- Conformance Test

Reference ImplementationやSampleは仕様要求と区別します。
概要ノートをそのまま事実Sourceにせず、技術的な詳細は一次情報で再確認します。

## 5. Mechanism Knowledge Mapを作る

概要の理解ポイントと一次情報を合わせ、必要な技術要素を抽出します。

- 入力 / 出力
- Actor / Component
- Request / Response / Event
- Data Object
- Field / Identifier
- State / Transition
- 検証
- 判断
- 変換
- Binding
- Signature / Proof
- Authentication / Authorization
- Storage
- 実処理
- 外部境界
- 信頼境界
- Invariant
- Failure Condition
- Recovery / Retry
- Replay / Idempotency
- Ordering / Concurrency
- 実際に拒否できる場所
- Protocol Requirement
- Implementation Choice
- Version / Status

このKnowledge Mapから、補足が必要な用語を**Mechanism Term Ledger**へ抽出します。

最低限次を追跡します。

| 項目 | 内容 |
|---|---|
| Term | 用語・略語・Field・Claim・重要Concept |
| First Appearance | 初登場箇所 |
| Why Reader Needs It | その語を理解しないと何が追えないか |
| Needs Toggle | Yes / No |
| Toggle Location | 対応する`<details>`の位置 |
| Toggle Status | Covered / Missing / Not Needed |
| Main-text Responsibility | トグルへ隠さず本文に残す説明 |

`Needs Toggle = Yes`の語は、対応するトグルを置くまでDraft完成扱いにしません。

## 6. Data Flow Mapを作る

仕組みノートでは、主要Dataについて必ず生成から利用まで追います。

各重要Dataについて最低限、次を対応付けます。

`誰が生成 → 何を含む → 誰へ送る → どこで検証 → どの判断に使う → どこへ保存 → 次に何へ渡す`

Fieldを紹介するだけで終わってはいけません。
Fieldが後続処理のどこで使われるかまで追います。

## 7. Architecture Mapを作る

OverviewのRoleを、実装Componentへ降ろします。

必要に応じて次を整理します。

- Client / UI
- Agent / LLM
- Backend
- Verifier
- Policy / Constraint Evaluator
- Credential / Key Service
- Storage
- External Provider
- Payment / Commerce System
- Side Effect API
- Audit / Receipt Store

各Componentについて、入力、出力、責任、保持State、Secret、外部接続、信頼境界を整理します。

RoleとProcessが1対1でない場合は、その違いを明示します。

## 8. Causal GraphとInvariant / Boundary Mapを作る

重要な流れでは、次が切れていないことを確認します。

`Data → 検証・比較 → 判断 → 状態変更または実処理`

また、必要に応じて次を区別します。

- 識別。
- 本人確認。
- 暗号学的な検証。
- 権限判断。
- 信頼判断。
- 資金決済。
- 業務上の成功。

各Invariantについて、守る仕組み、実際に拒否できる場所、失敗時の結果を対応付けます。

## 9. Official Mechanism Coverage Matrixを作る

公式仕様の主要Mechanismを意味単位へ分解します。

| 項目 | 内容 |
|---|---|
| Source | 公式資料の章・節・Schema・Reference Implementation |
| Mechanism Point | 再構成すべき内部動作 |
| Type | Data / Flow / Architecture / State / Validation / Security / Failure / Implementation |
| Importance | Critical / Major / Minor / Reference-only |
| Article Location | 対応Section |
| Status | Covered / Partial / Missing / Intentionally Out |
| Reason | 判定理由 |

重要Mechanismの`Covered`は、記事だけで`入力 → 処理主体 → 検証・変換 → 状態または出力 → 目的 → 失敗`を追える場合に限ります。

## 10. Client Question Coverage Matrixを作る

最低限次を持ちます。

| 項目 | 内容 |
|---|---|
| Question | クライアントや実装者の質問 |
| Category | Data / Flow / Architecture / Security / State / Failure / Implementation / Integration / Scope |
| Required Knowledge | 答えるために必要な知識 |
| Importance | Critical / Major / Minor |
| Article Location | 対応Section |
| Status | Covered / Partial / Missing |
| Reason | 判定理由 |

**「仕様を網羅した」だけでは完成ではありません。**
主要なクライアント質問へ記事だけで理由付き回答ができる必要があります。

## 11. 中心質問と理解ストーリーを作る

ここまで整理してから記事全体を束ねる中心質問を決めます。

仕様書順ではなく、概要ノートから自然に深掘りできる順にします。

基本形は、

`概要で見た全体像 → 実際のData → 通信 → 検証 → 状態 → アーキテクチャ → 実装 → Failure / Security → 全体再接続`

です。
ただし固定Templateにはしません。

## 12. Visual Representation Planを作る

本文を書く前に、どの複雑さをMarkdown Table、Mermaid、Payload例で外部化するか決めます。

特に次は図を検討します。

- Component Architecture。
- End-to-End Sequence。
- Data Binding Chain。
- State Transition。
- Verification Pipeline。
- Trust Boundary。
- Failure / Retry Flow。

図の枚数Quotaは持ちません。
複雑な関係を文章だけで読者へ再構築させないことを優先します。

## 13. 本文を書く

概要ノートの説明を繰り返すだけにしません。
概要で説明済みのConceptは短く再確認し、すぐに技術的な深掘りへ進みます。

中心Mechanismでは必要に応じて次をつなげます。

1. 概要では何として説明したか。
2. 実際にはどんなDataがあるか。
3. 誰が生成するか。
4. どこへ送るか。
5. 何を検証・比較するか。
6. どの状態や保存Dataが関係するか。
7. どこで許可・拒否するか。
8. どんなComponent構成になるか。
9. 実装では何を作るか。
10. 失敗時に何が起きるか。
11. なぜその設計で概要の目的を達成できるか。

Mechanism Term Ledgerで`Needs Toggle = Yes`の用語は、初出付近に`<details>`トグルを配置します。
FieldやClaimをトグルで補足する場合でも、そのFieldが後続処理のどこで使われるかは本文へ残します。

## 14. Overview整合性チェック

Draft完成後、概要ノートと仕組みノートを並べて確認します。

- Role名が一致しているか。
- Flowの順序が矛盾していないか。
- 概要で保証していないことを仕組み側で保証していないか。
- 仕組み側で新たに分かった重要Boundaryが概要にも必要ではないか。
- 同じ概念を違う意味で使っていないか。
- 概要側で補足トグルが必要な共通用語なのに未説明ではないか。

必要なら概要ノート側も修正対象にします。

## 15. 日本語可読性チェック

各Sectionについて次を確認します。

- 英語の抽象語へ依存していないか。
- API / Field名以外の英語が連続していないか。
- 日本語だけでも主要な因果関係を追えるか。
- MermaidやTableも日本語で読めるか。
- 補足が必要な用語が外部検索なしで読めるか。
- `Needs Toggle = Yes`かつ`Toggle Status = Missing`が0か。

## 16. Interrogation / Review Loop

Draft後は`.codex/skills/mechanism-interrogate/SKILL.md`で全文を破壊テストし、その後`.codex/skills/mechanism-review/SKILL.md`で全文レビューします。

毎Round、次を再評価します。

- Overview → Mechanism Traceability Matrix
- Official Mechanism Coverage Matrix
- Client Question Coverage Matrix
- Data Flow Map
- Architecture Map
- Invariant / Boundary Map
- Visual Representation Plan
- Mechanism Term Ledger / Toggle Status

## 17. No-change Final Round

Completion前に変更なし最終Roundを1回通します。

このRoundでは`Needs Toggle = Yes`の全用語に対応するトグルがあり、重要説明がトグルだけへ隠れていないことも確認します。

## Completion

以下をすべて満たすまで完了としません。

- 概要ノートのCritical / Majorな理解ポイントが仕組みノートへ追跡可能
- Official Mechanism CoverageのCritical / MajorにPartial / Missingが0
- Client Question CoverageのCritical / MajorにPartial / Missingが0
- 主要Dataを生成から最終利用まで追える
- 主要Componentの責任、通信、保持State、信頼境界を説明できる
- 重要Invariantに仕組み / 拒否箇所 / Failureが対応している
- 複雑な関係が適切なMarkdown / Mermaidで外部化されている
- 日本語だけでも主要な因果関係を追える
- Mechanism Term Ledgerの`Needs Toggle = Yes`かつ`Toggle Status = Missing`が0
- 補足が必要なField / Claim / Security用語を外部検索なしで理解できる
- 重要Requirementや拒否条件をトグルだけへ隠していない
- Overviewとの矛盾がない
- Interrogation Critical = 0
- Interrogation Major = 0
- Review Critical = 0
- Review Major = 0
- 必要な再Interrogation / 再Reviewが完了
- 変更なし最終Roundを1回通過

## 保存

成果物はMarkdownノートです。
既存ノート更新では特別な理由がなければURLとIDを維持します。
意味のある更新ではFront Matterの`reviewed_at`と`_data/article_changes.yml`を更新します。