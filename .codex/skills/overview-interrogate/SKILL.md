---
name: overview-interrogate
description: Overview Draftを読者・実装者・Security・仕様厳密性の視点から破壊テストし、各Concept / Evidenceについて「何が分かるか・何は分からないか・どの判断に使うか」まで説明し、複雑な関係が適切に可視化される状態へ収束させる。
---

# Overview Interrogate

このSkillはFAQ生成ではなく、Overview Draftを読者の質問で破壊テストするための反復Skillです。
Interrogationは1回では終えません。
修正後は変更箇所だけでなく全文を再評価します。

## 事前確認

最初に以下を読みます。

- `.codex/skills/COMMON.md`
- `.codex/skills/MARKDOWN.md`
- `.codex/skills/overview-note/SKILL.md`
- `.codex/skills/overview-review/SKILL.md`
- 対象Draft全文
- 対象Versionの公式Specification、Schema、Security、Flow、Status
- 利用可能な実読者の質問、過去Q&A、レビュー指摘
- Term / Concept Ledger
- Visual Representation Plan

## Coverage Matrix

### Official Specification Coverage Matrix

公式仕様の主要なRole、Concept、Data、Evidence、Flow、Verification、Security、Failure、Scope、Extensionを意味単位に分解します。

| 項目 | 内容 |
|---|---|
| Source | 公式資料の章・節・Schema |
| Knowledge Point | 読者が理解すべき事実・関係 |
| Importance | Critical / Major / Minor / Reference-only |
| Article Location | 記事の対応Section |
| Status | Covered / Partial / Missing / Intentionally Out of Overview |
| Reason | Status判定の理由 |

`Covered`は同じ単語が出ているだけでは認めません。
重要Concept / Evidenceでは、記事だけで必要に応じて次を説明できる必要があります。

`何なのか → 何を観測・表現するか → そこから何が分かるか → 何は分からないか → 後続の何の判断に使うか → なぜ必要か`

このChainが途中で切れていればPartialまたはMajorです。

### Reader Question Coverage Matrix

実際の読者質問、過去Q&A、レビュー指摘を質問・理解ポイント単位へ分解します。
実質問がない場合でもKnowledge Mapから初期質問を作ります。

重要Conceptごとに最低限、次の追質問を検討します。

- 「それは何？」
- 「それで具体的に何が分かるの？」
- 「その証拠が正しくても何は分からないの？」
- 「次に何の判断へ使うの？」
- 「似たEvidenceと何が違うの？」
- 「それが無いと何を誤判定するの？」

重要なPartial / Missingが残る状態で完了しません。

## Interrogation Persona

### 初学者

- それは結局何か。
- なぜ必要か。
- 名前や例を並べただけになっていないか。
- その説明から自分は何を理解すべきなのか。
- 新しい専門語を別の未知語だけで説明していないか。

### 実装者

- 誰が生成するか。
- 誰が保持・送信・検証するか。
- どの順番で処理するか。
- 前StepのOutputは次Stepで何に使われるか。
- Verification Resultが具体的にどのDecisionへ入るか。
- 主要Fieldは何をBinding / Identificationしているか。

### Security

- そのEvidenceが証明する範囲はどこまでか。
- そのEvidenceだけでAuthorizationまで結論していないか。
- Identity、Runtime、Integrity、Authority、Reputationなど別の問いを混同していないか。
- Agentが嘘をついた時、どのEvidenceで何だけ検知できるか。
- 何をTrustしているか。

### 仕様厳密性

- Protocol独自か既存標準利用か。
- MUST / SHOULD / MAYのどれか。
- Version固有か。
- Scope内かScope外か。
- 実装例を仕様として断定していないか。
- 一般例を公式仕様のFeatureとして書いていないか。

### System Integration

- 既存Systemの何を置き換えるか、置き換えないか。
- 各Roleへ何を実装する必要があるか。
- そのConceptが実際のArchitecture上どこへ入るか。

## Explanatory Closure Test

各主要Sectionで、名詞・箇条書き・Tableを一度隠して本文だけを読みます。
次へ答えられるか確認します。

1. このSectionの結論は何か。
2. 列挙された各要素は別々に何を確認するものか。
3. 各要素のResultからどこまで結論できるか。
4. 各要素だけでは何を結論できないか。
5. そのResultは次のFlow / Policy / Verificationへどう使われるか。

例えば、

- Workload Identity
- TEE Attestation
- Software Provenance
- Binary Digest

を並べただけで「Runtime Evidenceを使う」と結論しているSectionはMajorです。
それぞれが答える問いと限界が違うためです。

## List / Table破壊テスト

ListやTableは情報を整理する手段であり、説明そのものではありません。
次はMajorです。

- 例を6個並べたが、なぜその6個が必要なのか説明しない。
- 列名が`Evidence / 用途`だけで、何が検証できるか不明。
- 本文がListを言い換えただけ。
- 読者がList中の用語を自分で調べないとSectionの意味が分からない。

必要なら「Evidence | 何を確認する | 分かること | 分からないこと | Policyでの利用」のように分解します。

## Orphan Term Test

Term / Concept Ledgerを使い、重要語が初登場だけして放置されていないか確認します。

次はMajorです。

- 一度だけ出て以後説明も利用もされない重要語。
- 略語を導入したが意味を回収しない。
- 似た語を増やしただけで差を説明しない。
- 後続Flowで使わない概念を専門性の演出として追加している。

## Visual Coverage破壊テスト

Visual Representation Planと本文を照合し、複雑な関係を読者の頭の中だけで再構築させていないか確認します。

特に次を確認します。

- Actor / Roleが3者以上関係するなら、責任関係やFlowを図にした方が明確ではないか。
- 複数Stepの通信はSequence Diagramが必要ではないか。
- Data / EvidenceのBinding ChainはFlowchartが必要ではないか。
- State TransitionはState Diagramが必要ではないか。
- Policy / Verificationの分岐はFlowchartが必要ではないか。
- Trust Boundary / Security Boundaryが文章だけで曖昧になっていないか。
- 全体図1枚だけで、中心Mechanismの複雑さを押し込めていないか。

図にすると理解が大きく改善するCritical / Majorな関係が文章だけで残っていればMajorです。

逆に、単純な1対1関係を無理に図にして本文と重複するだけなら整理します。

Mermaidを一時的に隠して本文だけでも意味が分かる必要があります。
一方で本文を読んだ後にMermaidを見ることで、関係・順序・分岐がより速く正確に把握できる状態を目指します。

## Question Chain

重要Conceptでは単発質問で終わらせません。

`何か → なぜ必要か → 何を観測するか → Resultから何が分かるか → 何は分からないか → 誰が使うか → どの判断へ入るか → 失敗 / 不一致なら何が変わるか`

対象を誤解せず説明できる深さまで掘ります。

## Severity

### Critical

事実誤認、中心Mechanism破綻、Security上危険な過剰解釈、主要Flow矛盾です。

### Major

- 重要Conceptが名前・定義・例の列挙で止まっている。
- 「それで何が分かるの？」へ答えられない。
- Evidenceの意味と限界を混同している。
- Verification Resultが後続判断へ接続されていない。
- Reader Question Coverageの重要Gapがある。
- Critical / Majorな複雑関係の可視化が不足している。
- 重要な孤児用語が残っている。

### Minor

中心理解を壊さない局所的な不足です。

## Loop

1. 2つのCoverage Matrixを作る。
2. Term / Concept Ledgerを確認する。
3. Visual Representation Planを確認する。
4. Draft全文をPersonaごとにInterrogateする。
5. Explanatory Closure Testを主要Sectionへ実施する。
6. List / Table破壊テストを実施する。
7. Orphan Term Testを実施する。
8. Visual Coverage破壊テストを実施する。
9. Critical / MajorとPartial / Missingを集約する。
10. 一次情報へ戻って修正する。
11. 必要ならKnowledge Map、関係モデル、理解ストーリー、見出し、Visual Planから作り直す。
12. 修正後全文を最初から再Interrogateする。
13. Matrix、Ledger、Visual Planを更新する。
14. 新しい説明から二次・三次質問を導出する。
15. Critical / Majorと重要なPartial / Missingが0になるまで繰り返す。

## Reviewとの相互Loop

Interrogation収束後に`overview-review`を実行します。
ReviewでFact、Boundary、Flow、Data、Security、Structure、Coverage、説明の閉じ方、Visual Representationへ影響する修正が入った場合、Matrix / Ledger / Visual Plan更新 → 再Interrogation → 必要なら再Reviewへ戻ります。

## No-change Final Round

完成前に変更なし最終Roundを1回通します。

- Official CoverageのCritical / MajorがCoveredか。
- Reader Question CoverageのCritical / MajorがCoveredか。
- Term / Concept LedgerのCritical / Majorな未解決語が0か。
- 重要Concept / Evidenceについて「何が分かるか・何は分からないか・何の判断に使うか」が説明できるか。
- ListやTableに説明を丸投げしていないか。
- Critical / Majorな複雑関係が適切に可視化されているか。
- Review Critical / Major = 0か。
- Fact / Boundary確認で変更不要か。

このRoundで本文または重要Statusが変わった場合はNo-changeではありません。

## Completion Condition

以下をすべて満たした時だけ完了です。

- Interrogation Critical = 0
- Interrogation Major = 0
- Review Critical = 0
- Review Major = 0
- Official Specification Coverage MatrixのCritical / MajorにPartial / Missingが0
- Reader Question Coverage MatrixのCritical / MajorにPartial / Missingが0
- 重要Concept / Evidenceの説明が意味・限界・後続判断まで閉じている
- 名称や例の列挙だけで終わる主要Sectionがない
- Term / Concept LedgerのCritical / Majorな未解決語が0
- Critical / Majorな複雑関係が適切なMarkdown / Mermaidで外部化されている
- 必要な再Interrogation / 再Reviewが完了している
- 変更なし最終Roundを1回通過している
