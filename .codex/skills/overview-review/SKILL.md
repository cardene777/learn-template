---
name: overview-review
description: 概要ノートを、Coverage、Facts、Boundary、説明品質、各Concept / Evidenceの意味と限界、後続判断への接続、複雑な関係の可視化まで含めてレビューする。
---

# Overview Review

概要ノートを「項目が揃っているか」ではなく、初見の技術者が対象の全体像を理由付きで説明できるかでレビューします。
Review自体もCritical / Majorが0になるまで繰り返し、Review修正後は必要に応じてInterrogationへ戻します。

## 事前確認

- `.codex/skills/COMMON.md`
- `.codex/skills/MARKDOWN.md`
- `.codex/skills/overview-note/SKILL.md`
- `.codex/skills/overview-interrogate/SKILL.md`
- 対象ノート全文
- 対象Versionの公式資料
- Official Specification Coverage Matrix
- Reader Question Coverage Matrix
- Term / Concept Ledger
- Visual Representation Plan

2つのCoverage Matrix、Term / Concept Ledger、Visual Representation Planがない場合はReview未完了です。

## 最重要Review: 説明が閉じているか

中心Concept / Evidence / Security Controlについて、必要に応じて次を本文だけで説明できるか確認します。

1. 何なのか。
2. 何を観測・表現しているのか。
3. 検証成功や値の存在から何が分かるのか。
4. その情報だけでは何は分からないのか。
5. 後続のどの判断・Flowへ使うのか。
6. なぜ必要なのか。

この接続が無い重要ConceptはMajorです。

例えば`Runtime Evidence`のSectionで、`Workload Identity / TEE Attestation / Software Provenance / Binary Digest`を列挙しただけならMajorです。
これらはそれぞれ別の問いへ答えるEvidenceであり、「Runtimeが安全」という一つの結論へまとめてはいけません。

## Coverage Matrix Review

### Official Specification Coverage Matrix

Critical / Majorについて次を確認します。

- Sourceが正しいか。
- Knowledge Pointが粗すぎないか。
- Article Locationが実際に説明しているか。
- Covered判定が名称一致ではないか。
- Conceptの意味、限界、関係まで説明されているか。
- Partial / Missingが残っていないか。

### Reader Question Coverage Matrix

Critical / Major質問について、記事だけで理由を含めて答えられるか確認します。
特に次の質問を重視します。

- 「それで何が分かるの？」
- 「それだけでは何は分からないの？」
- 「そのResultを何の判断に使うの？」
- 「似たEvidenceと何が違うの？」

## Knowledge Coverage

公式資料とノートを照合し、主要なProblem、Role、Concept、Data / Evidence、Important Field / Identifier、Flow、Capability、Constraint、Security / Trust、Verification、Failure、Non-goal、Extension、Comparison、Integrationが必要なのに欠落していないか確認します。

主要Fieldは、名前だけではなく何をBinding / Identification / Versioning / Delegation / Scopingするか、そしてその結果が何の判断へ使われるか説明できる必要があります。

## Term / Concept Ledger Review

重要語について、初登場から説明・後続利用まで追います。

次はMajorです。

- 初登場だけして回収されない重要語。
- 略語だけ導入して意味を説明しない。
- 似た概念を複数出すが差を説明しない。
- 後続Flowで使わない専門語を増やしている。

## List / Table Review

ListやTableは整理手段であって、説明の代替ではありません。
次はMajorです。

- 名称や例を並べた後、各項目の意味を説明しない。
- `Evidence | 用途`のような抽象的な表だけで「何が確認できるか」が不明。
- Tableを読んでも各Evidenceの違い・限界が分からない。
- 本文がTableを言い換えるだけ。
- 読者が外部検索しないとSectionの結論を理解できない。

必要なら、`Evidence | 何を確認する | 分かること | 分からないこと | 後続判断`まで分解します。

## Visual Representation Review

Visual Representation Planと本文を照合し、複雑な関係が適切に外部化されているか確認します。

図の枚数ではなく、読者が関係を正確に把握できるかで判定します。

次はMajorです。

- Actor / Roleが複数いるのに、誰が誰へ何を渡すか文章だけで追いづらい。
- End-to-End Flowが長いのにSequence Diagram等がない。
- Data / EvidenceのBinding Chainが文章だけで、結び付きが見えない。
- State Transitionがあるのに状態と遷移条件が見えない。
- Policy / Verificationの分岐が複雑なのに文章だけで追わせる。
- Trust Boundary / Security Boundaryが図にすると明確になるのに曖昧なまま。
- 全体図1枚だけ置き、中心Mechanismの詳細な関係を本文へ押し込んでいる。

反対に、図を増やすこと自体を品質とはみなしません。
単純な1対1関係や本文と完全に重複する図は整理します。

Mermaidは本文の代替ではありません。
図を一時的に隠しても本文だけで意味が分かり、図を見ると関係・順序・分岐をより速く把握できる状態が理想です。

## 見出し階層

H2 / H3 / H4だけを読み、理解の流れが推測できるか確認します。
用語辞典のように平坦でないか、細分化しすぎて説明が途切れていないか確認します。

## 説明品質

普通に「初学者向けに詳しく説明して」と依頼した時の説明を基準にします。
以下はMajorです。

- Skill適用後の方が薄い。
- 定義を数文書いて図やTableへ逃げる。
- なぜ必要か、なぜ成立するかが分からない。
- Concept同士の因果関係が分からない。
- 重要Conceptに「何が分かるか」の説明がない。
- 重要Conceptに「何は分からないか」がなく、過剰解釈できる。
- Mermaid追加の代わりに本文が短くなっている。

## Interrogation Coverage

主要Conceptについて必要に応じて次へ本文だけで答えられるか確認します。

- 何か。
- なぜ必要か。
- 誰が生成するか。
- 誰が署名・保持・送信・検証するか。
- Flow上いつ登場するか。
- 何を観測・表現しているか。
- Resultから何が分かるか。
- Resultだけでは何は分からないか。
- 前StepのOutputが次Stepでどう使われるか。
- 何をTrustし、何を決定的に検証するか。
- Protocol ScopeとApplication責任の境界。
- 失敗時に何が起きるか。

中心理解に必要なのに答えられない場合はMajorです。

## Facts and Boundary

追加された断定を一次情報へ戻して再検証します。
特にVersion / Status、Role / Responsibility、Required / Optional、MUST / SHOULD / MAY、Field / Schema、Verification Rule、Failure Handling、標準Flowと独自実装例の境界を確認します。

Evidenceの説明で「検証できること」を過大に書くのはCriticalまたはMajorです。
例として、Workload Identityが正しいからSoftwareのIntegrityも保証される、TEE Attestationが成功したからAction Authorityもある、という説明は誤りです。

## Flowと実装責任

主要Roleがある技術では、各RoleのInput / Output、Authoritative Data、VerificationをどこでEnforceするか、Protocolが具体的APIを定めない場合に何を標準化しているかを確認します。

## Mermaid / Markdown

Mermaidを一時的に無いものとして本文を読み、主要Concept / Flowが本文だけでも理解できるか確認します。
図は補助であり本文の代替ではありません。

Diagram Typeも確認します。

- 通信順序はSequence Diagramが自然か。
- 状態遷移はState Diagramが自然か。
- Binding / Policy / BoundaryはFlowchartが自然か。
- 比較はTableの方が自然ではないか。

Mermaidを書く場合は公式Introと使用Diagram Typeの公式Syntaxを確認します。

## Review修正後の再Interrogation

Fact、Role、Flow、Field、Security / Trust、Scope、新Concept、大きな構成、Coverage、説明の意味・限界、Visual Representationを変更した場合は、修正後全文を`overview-interrogate`へ戻します。

## No-change Final Round

Completion直前に、変更なし最終Roundを実行します。

- 2つのCoverage MatrixのCritical / MajorにPartial / Missingがない。
- Term / Concept LedgerのCritical / Majorな未解決語が0。
- 重要Concept / Evidenceの説明が意味・限界・後続判断まで閉じている。
- 名称・例・Tableの列挙だけで終わる主要Sectionがない。
- Critical / Majorな複雑関係が適切なMarkdown / Mermaidで外部化されている。
- 新しいCritical / Majorな質問が出ない。
- Facts / Boundary再確認で修正不要。
- Review Critical / Major = 0。
- Interrogation Critical / Major = 0。

このRoundで重要な修正が発生した場合、修正後に再度最終Roundを実行します。

## Severity

### Critical

事実誤認、Security上危険な説明、Evidenceから導けない保証の断定、主要Flow破綻、公開不可情報の混入です。

### Major

読者理解に影響する問題、重要Conceptが列挙止まり、Evidenceの意味・限界不足、Matrixの重要Partial / Missing、Interrogation未収束、重要な可視化不足、重要な孤児用語です。

### Minor

中心理解を壊さない局所的な表現問題です。

## Completion

以下をすべて満たすまで終了しません。

- Review Critical = 0
- Review Major = 0
- Interrogation Critical = 0
- Interrogation Major = 0
- Official Specification Coverage MatrixのCritical / MajorにPartial / Missingが0
- Reader Question Coverage MatrixのOverview範囲Critical / MajorにPartial / Missingが0
- 重要Concept / Evidenceについて「何が分かるか・何は分からないか・何の判断に使うか」を説明できる
- 主要Sectionが名称や例の列挙で終わっていない
- Term / Concept LedgerのCritical / Majorな未解決語が0
- Critical / Majorな複雑関係が適切なMarkdown / Mermaidで外部化されている
- 必要な再Interrogation / 再Reviewが完了している
- 変更なし最終Roundを1回通過している

Reviewで本文へ意味のある修正を保存した場合は、Front Matterの`reviewed_at`と必要な`_data/article_changes.yml`を更新します。
