---
name: mechanism-review
description: 仕組みノートを、概要ノートとの対応、クライアント質問への回答力、データ、通信、アーキテクチャ、実装、Security、Failure、日本語の分かりやすさまで含めて全文レビューする。
---

# Mechanism Review

## Goal

仕組みノートを、情報量や図の枚数ではなく、**概要で理解した内容を技術レベルまで一貫して深掘りし、クライアントや実装者の深い質問へ記事だけで答えられるか**でレビューします。
問題があればCommentだけ残さず本文を直接修正します。

## Required

レビュー前に次を読みます。

- `.codex/skills/COMMON.md`
- `.codex/skills/MARKDOWN.md`
- `.codex/skills/mechanism-note/SKILL.md`
- `.codex/skills/mechanism-interrogate/SKILL.md`
- 対象技術の完成済み概要ノート
- 対象仕組みノート全文
- Overview → Mechanism Traceability Matrix
- Official Mechanism Coverage Matrix
- Client Question Coverage Matrix
- Data Flow Map
- Architecture Map
- Invariant / Boundary Map
- Visual Representation Plan

概要ノートが存在するのに読んでいない、またはTraceability Matrixがない場合はReview未完了です。

## 1. 概要との連続性Review

まず概要ノートと仕組みノートを並べて確認します。

- 概要で重要だったRole、Concept、Flowが仕組み側でも追跡できるか。
- 概要で説明した順序や因果関係と矛盾していないか。
- 概要で保証していないことを仕組み側で保証していないか。
- 概要のConceptを別の意味で使っていないか。
- 概要の重要ポイントを仕組み側で理由なく落としていないか。
- 仕組み調査で見つけた重要Boundaryが概要にも必要ではないか。

重要なOverview Pointが技術的に展開されていなければMajorです。

## 2. クライアント質問Review

Client Question Coverage MatrixのCritical / Majorについて、記事だけで理由付き回答ができるか確認します。

特に次を確認します。

### Data

- 実際に何を送受信するか。
- 誰がPayloadを作るか。
- 必須FieldとOptional Fieldは何か。
- どのFieldが後続判断で使われるか。
- 何と何をBindingしているか。

### Flow

- どの主体がどの順で通信するか。
- 前StepのOutputが次Stepの何に使われるか。
- どこで分岐・Retry・Rejectするか。

### Architecture

- どのComponentが必要か。
- 各Componentの責任、入力、出力、保持Stateが分かるか。
- Client / Backend / Agent / Verifier / External Serviceをどう分けるか。
- Trust Boundaryが分かるか。

### Implementation

- 最低限何を実装するか。
- 何を保存するか。
- Key / Credential / Secretをどこへ置くか。
- 既存Systemのどこへ組み込むか。
- PoCとProductionで責任がどう違うか。

### Security / Failure

- 改ざんや流用をどこで検知するか。
- SignatureがValidでもRejectされる条件が分かるか。
- 失敗時に実処理が止まるか。
- Retry / Duplicate / Concurrent Request時に何が起きるか。
- 後から原因を追えるDataが分かるか。

主要質問へ答えられない場合は、仕様Coverageが埋まっていてもMajorです。

## 3. Data Flow Review

重要Dataごとに次を追います。

`生成者 → 内容 → 送信先 → 検証箇所 → 判断への利用 → 保存 → 次の利用`

次はMajorです。

- JSONやField一覧を載せただけで後続処理へ接続しない。
- 同じTransactionを結び付けるFieldが不明。
- Signature / Hashの対象が曖昧。
- どのByte列やObjectを検証するのか不明。
- RequestとResponseの対応が追えない。

## 4. Architecture Review

Role説明だけで終わらず、実装Componentまで降りているか確認します。

各主要Componentについて、必要に応じて次が分かる必要があります。

- 入力。
- 出力。
- 責任。
- 保存State。
- Secret / Key。
- 外部接続。
- Trust Boundary。
- 実際に拒否できる場所。

RoleとProcessが1対1でない場合、その違いを説明します。

## 5. 再構成Test

本文を閉じた後でも、読者が次を日本語で説明できるか確認します。

- 概要で見た全体像。
- 実際に流れるData。
- 誰がそのDataを作るか。
- どの順序で通信するか。
- どこで何を検証するか。
- どの状態を保存するか。
- どこで許可・拒否するか。
- どこで購入確定や課金が起きるか。
- どのComponentを実装するか。
- 失敗した時に何が残るか。

中心Mechanismを説明できなければMajorです。

## 6. 因果関係Review

「Aの次にBをする」だけでは不十分です。
必要な箇所では次を説明します。

- BはAのどのDataを使うか。
- なぜBが必要か。
- Bを省略すると何が壊れるか。
- Bの結果が次の処理へどう影響するか。
- BはどのInvariantを守るか。

## 7. Coverage Review

### Overview → Mechanism Traceability

Critical / MajorなOverview Pointが仕組み側のSectionへ対応しているか確認します。
`Intentionally Not Expanded`には明示的な理由が必要です。

### Official Mechanism Coverage

Critical / Majorは記事だけで次を追える場合のみCoveredです。

`入力 → 処理主体 → 検証・変換 → 判断 → 状態または出力 → 目的 → 失敗`

### Client Question Coverage

Critical / Majorへ記事だけで回答できる場合のみCoveredです。
単語が存在するだけではCoveredにしません。

## 8. Boundary / Failure / Security Review

識別、本人確認、暗号学的な検証、権限判断、信頼判断、資金決済、業務上の成功を混同しません。

重要なFailureでは、何が成立しないか、どこで検知するか、実処理は止まるか、何が保存されるか、Retry可能かを追います。

正しい判断をしていても、その判断を迂回して購入確定や課金へ到達できるならMajorです。

## 9. Markdown / Mermaid Review

図は本文の代わりではありませんが、複雑な関係を文章だけで読者へ再構築させません。

次を確認します。

- End-to-End通信はSequence Diagramで追えるか。
- Data BindingはFlowchart等で追えるか。
- 状態遷移はState Diagramが適切か。
- Component構成とTrust Boundaryが見えるか。
- 図と本文のData、順序、名称が一致するか。
- MermaidのLabelが日本語で理解できるか。

## 10. 日本語可読性Review

技術的に正しくても、英語の抽象語へ依存して読みにくい場合はMajorです。
正式名称、Protocol名、Role名、API名、Field名、Claim名、Schema名は必要に応じて残します。

日本語本文だけで主要な因果関係を追える必要があります。

## Loop

Critical / Majorが0になるまで本文修正と全文Reviewを繰り返します。
修正後は次を更新し、全文を再Interrogateします。

- Overview → Mechanism Traceability Matrix
- Official Mechanism Coverage Matrix
- Client Question Coverage Matrix
- Data Flow Map
- Architecture Map
- Invariant / Boundary Map

## No-change Final Round

最後に本文を変更せずに済むRoundを1回通します。

## Completion

以下をすべて満たした時だけ完了です。

- OverviewとのCritical / Majorな対応漏れが0
- Official Mechanism CoverageのCritical / MajorにPartial / Missingが0
- Client Question CoverageのCritical / MajorにPartial / Missingが0
- 主要Dataを生成から利用まで追える
- 主要Architectureを実装Component単位で説明できる
- 主要Invariantに仕組み / 拒否箇所 / Failureが対応している
- 日本語だけで中心Mechanismを説明できる
- 複雑な関係が適切に可視化されている
- Overviewとの矛盾がない
- Review Critical = 0
- Review Major = 0
- Interrogation Critical = 0
- Interrogation Major = 0
- 必要な再Interrogation / 再Reviewが完了
- 変更なし最終Roundを通過
