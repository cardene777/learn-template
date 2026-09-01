---
name: overview-note
description: 一次情報からKnowledge Map、関係モデル、Coverage Matrix、理解ストーリーを設計し、各概念を「何が分かるか・何は分からないか・どの判断に使うか」まで閉じ、補足が必要な用語をMarkdownトグルで説明し、複雑な関係をMarkdown / Mermaidで外部化する概要ノートを作成する。
---

# Overview Note

概要ノートは短い要約でも用語集でもありません。
初見の技術者が、対象について「何か、なぜ必要か、どう動くか、主要なConcept / Data / Evidenceが何を意味し、何を判断できるのか」を自分の言葉で説明できる状態を作ります。

低Levelな実装詳細はMechanism Noteへ譲って構いませんが、全体理解に必要なMechanism、主要Data Shape、Binding、Verification、Trust、責任分担はOverviewでも省略しません。

## 最重要原則: 名前を出しただけでは説明したことにならない

Concept、Evidence、Field、Role、Mechanism、Security Controlを本文へ出した場合、重要なものについては必要に応じて次の説明を閉じます。

1. **何なのか** — その要素の役割を平易な言葉で説明する。
2. **何を観測・表現しているのか** — どの事実や状態についての情報なのか。
3. **そこから何が分かるのか** — 検証成功や値の存在から、どこまで結論できるのか。
4. **何は分からないのか** — そのEvidenceだけでは答えられない問いを明示する。
5. **次のどの判断に使うのか** — FlowやPolicyのどこへ入力されるのか。
6. **なぜ必要なのか** — これが無いとどんな誤判定やRiskが残るのか。

対象によって全部が必要とは限りませんが、中心Conceptでこの接続が切れている状態を`Covered`にしてはいけません。

例えば`Workload Identity`、`TEE Attestation`、`Software Provenance`を列挙するだけでは不十分です。
それぞれ「実行中のProcessのIdentity」「TEE内で期待した状態で起動したこと」「ArtifactがどのBuild Processから作られたか」のように答える問いが違うため、違いと後続判断への使い方まで説明します。

## 最重要原則: 補足が必要な用語はトグルで閉じる

初学者が本文を読む時に外部検索しないと意味を確定できない用語、略語、Role、Evidence、Protocol / Standard名、暗号・認証・認可用語、仕様固有Object、Version / Standardization Statusは、`.codex/skills/MARKDOWN.md`の「用語補足トグル」に従って初出付近へ`<details>`を置きます。

本文の主線には「この文脈で何をするものか」を短く残し、トグルには正式名称、平易な定義、なぜ登場するか、混同しやすい概念、保証すること / しないこと、短い例などを必要に応じて入れます。

重要な前提、主要Flow、Security Requirement、MUST / SHOULD / MAY、Version上の重大な差分をトグルだけへ隠してはいけません。

**補足が必要なのにトグルが無い用語を残したままOverviewを完成扱いにしてはいけません。**

## 最重要原則: 複雑な関係を読者の頭の中だけで組み立てさせない

本文だけで意味を説明できることは必須ですが、複数のActor、Data、Evidence、State、Decisionが関係する場合は、文章だけで読者に再構築させません。

次のような内容は、MermaidやMarkdown Tableで外部化した方が理解しやすいか必ず検討します。

- Actor / Roleの責任関係。
- End-to-Endの処理順。
- Data / Evidenceの生成元と利用先。
- Binding / Delegation / Authorityの連鎖。
- 状態遷移。
- PolicyやVerificationの分岐。
- Trust Boundary / Security Boundary。
- 複数Conceptの責任分離。
- 「前の確認結果が次の判断へ入る」という因果関係。

図の枚数Quotaは持ちません。
ただし、重要な関係を図にすると理解が大きく改善するのに文章だけで残っている場合は、説明設計の不足です。

Mermaidは本文の代わりではありません。
**本文で意味・理由・限界を説明し、Mermaidで関係・順序・分岐を一目で追えるようにする**ことを基本にします。

## 執筆フロー

### 1. 共通ルールを読む

- `.codex/skills/COMMON.md`
- `.codex/skills/MARKDOWN.md`

Mermaidを使う場合は公式Introと使用Diagram Typeの公式Syntaxを確認します。

### 2. 読者と読後ゴールを定義する

指定がなければ、そのテーマを初めて学ぶ技術者を対象にします。
読後に必要に応じて次を説明できる状態を目指します。

- 何を解決する技術か。
- なぜ必要か。
- 全体としてどう動くか。
- 主要Actor、Concept、Data、Evidenceがどう関係するか。
- 各Evidenceから何が分かり、何は分からないか。
- Dataを誰が生成・署名・利用・検証するか。
- Verification Resultが後続の何の判断に使われるか。
- 何を保証し、何を保証しないか。
- Scope外は何か。
- 類似技術との違い。
- 他技術との組み合わせ方。

### 3. 一次情報を調査する

記事構成を決める前に、対象Versionの公式Specification、Concept、Architecture、Schema、Security、Flow、FAQ、Statusを調査します。
比較を書く場合は比較対象も一次情報で確認します。
仕様書の章順をそのまま記事構成へ使いません。

### 4. Knowledge Mapを作る

必要に応じて次を抽出します。

- Problem / Motivation
- Actor / Role
- Concept
- Data / Evidence
- Important Field / Identifier
- Flow / Lifecycle
- Capability
- Constraint
- Security / Trust
- Verification
- Failure / Edge Case
- Non-goal / Out of Scope
- Extension
- Related Technology
- Comparison Target
- Version / Status

重要情報を「概要だから」という理由で捨てません。

各重要Concept / Evidenceには内部作業上、最低限次を対応付けます。

| 項目 | 内容 |
|---|---|
| Meaning | 何なのか |
| Observes / Represents | 何を観測・表現するか |
| Can Conclude | そこから何が分かるか |
| Cannot Conclude | 何は分からないか |
| Used By | 後続のどの判断・Flowで使うか |
| Why Needed | 無いと何が困るか |

この対応を作れない重要Conceptは、理解できていない可能性があるため一次情報へ戻ります。

### 5. Term / Concept Ledgerを作る

記事へ出す重要語を内部台帳で追います。

| 項目 | 内容 |
|---|---|
| Term | 用語・略語・重要Concept |
| First Appearance | 初登場箇所 |
| Meaning | 何なのか |
| Why Needed | なぜ必要か |
| Can / Cannot Conclude | 何が分かり、何は分からないか |
| Used Later | 後続のどこで使うか |
| Needs Toggle | 初学者向け補足トグルが必要か Yes / No |
| Toggle Location | 対応する`<details>`の配置箇所 |
| Toggle Status | Covered / Missing / Not Needed |
| Resolved | 記事内で説明が閉じているか |

`Needs Toggle = Yes`の語は、`.codex/skills/MARKDOWN.md`の正式記法で初出付近へトグルを置くまで`Resolved`にしてはいけません。

重要語が初登場だけして後続で回収されない状態、補足が必要なのにトグルが無い状態を許しません。

### 6. 関係モデルを作る

要素同士を、例えば次の関係として整理します。

- produces / consumes
- contains
- binds
- identifies
- signs
- verifies
- constrains
- authorizes
- delegates
- scopes
- observes
- proves / does not prove
- feeds decision
- extends
- differs from
- does not guarantee

Fieldについても「このFieldがAとBをBindingする」だけでなく、そのBindingが後続の何の判定に必要かまで整理します。

### 7. Official Specification Coverage Matrixの初版を作る

本文を書く前に、公式仕様の主要な章・Role・Concept・Data・Flow・Verification・Security・Failure・Scope・Extensionを意味単位へ分解します。
各行についてImportanceをCritical / Major / Minor / Reference-onlyで分類します。

`Covered`は単語が存在することではありません。
重要Concept / Evidenceについて、記事だけで「意味 → 分かること → 分からないこと → 後続判断との関係」を説明できる見込みがある場合だけCovered候補にします。

**Matrixを作らずに本文へ進んではいけません。**

### 8. Reader Question Coverage Matrixの初版を作る

実際の読者質問、過去Q&A、レビュー指摘がある場合は質問・理解ポイント単位へ分解します。
実質問がない場合でもKnowledge Mapから初期質問セットを作ります。

重要Conceptについては、少なくとも次の二次質問を検討します。

- 「それで具体的に何が分かるの？」
- 「それだけでは何は分からないの？」
- 「そのResultを次に何へ使うの？」
- 「似たEvidenceと何が違うの？」

### 9. 理解ストーリーを作る

Specification順や用語一覧ではなく、前の理解を使って次を理解できる順序へ並べます。
列挙Sectionが続く場合は、読者が「なぜこの一覧を見せられているか」を理解できる構造へ組み直します。

### 10. Visual Representation Planを作る

本文を書く前に、Knowledge Mapと関係モデルから「文章だけでは追いづらい関係」を抽出します。

各候補について、何を見せるための図かを決めます。

| 表現 | 向いている内容 |
|---|---|
| Flowchart | Concept関係、Data Binding、判断分岐、Trust Boundary |
| Sequence Diagram | 複数Actor間の通信順序、Request / Response |
| State Diagram | State Transition、Lifecycle |
| Markdown Table | 比較、責任分担、何が分かる / 分からないの整理 |
| JSON / Payload例 | Data ShapeやField関係 |

特に中心Mechanismについて、**全体像の図だけ1枚置いて終わりにしない**ようにします。
必要なら、全体図に加えて、通信、Binding、State、Policy、責任分離などを個別図へ分けます。

### 11. 見出し階層を先に完成させる

H2 / H3 / 必要な場合のみH4まで作ります。
H2は大きな理解単位、H3はその理解に必要な論点です。
Concept一覧を平坦に見出し化しません。

### 12. 本文を自然に詳しく書く

普通に「初学者向けに詳しく説明して」と依頼された時と同等以上の自然さと深さで説明します。

重要Conceptでは、名称や例の列挙で止めず、具体的に何を確認できるのかを文章で説明します。
表を使う場合も、列名だけで意味を圧縮しすぎず、その表から読者が得るべき結論を本文で説明します。

Term / Concept Ledgerで`Needs Toggle = Yes`とした語は、初出付近に`<details>`トグルを置きます。
本文の中心説明をトグルへ移動して短くしてはいけません。

Mermaidを置く場合は、図の直前または直後で「この図のどこを見るべきか」を本文で説明します。
図にだけ重要Factを置きません。

主要DataやFieldを知らないとBinding、Verification、責任分担を理解できない場合はOverviewでも簡潔なData Exampleを示します。
Markdown / Mermaidのために本文を削ってはいけません。

### 13. Coverage Matrixを本文へ紐付ける

Draft完成後、2つのMatrixへ実際のArticle LocationとStatusを記入します。
StatusはCovered / Partial / Missing / Intentionally Out of Overviewです。

中心Conceptで次のどれかが欠ける場合は原則Partialです。

- 何なのか分からない。
- 何を確認できるか分からない。
- 何を確認できないか分からないため過剰解釈できる。
- 後続Flow / Decisionとの接続がない。
- 類似Conceptとの差が分からない。
- 複雑な関係が文章だけで残り、読者が頭の中で再構築する必要がある。
- 補足が必要な用語なのに`<details>`がなく、外部検索しないと読めない。

### 14. Overview Interrogationを収束させる

`.codex/skills/overview-interrogate/SKILL.md`を実行します。
Critical / Majorと重要なPartial / Missingが0になるまで一次情報へ戻って修正し、全文を再Interrogateします。

### 15. ReviewとInterrogationを相互Loopさせる

Interrogation収束後に`.codex/skills/overview-review/SKILL.md`を実行します。
Review修正がFact、Boundary、Flow、Data、Security、Structure、Coverage、Visual Representation、Term Toggleへ影響する場合はMatrix / Ledger更新 → 再Interrogation → 必要なら再Reviewへ戻します。

### 16. 変更なし最終Roundを通す

Completion判定前に、本文を変更せずに済む最終Roundを1回通します。

確認対象は次です。

- Official Specification Coverage Matrix
- Reader Question Coverage Matrix
- Term / Concept Ledger
- `Needs Toggle = Yes`の全用語に対応する`<details>`があるか
- Visual Representation Plan
- 重要Concept / Evidenceの説明が閉じているか
- Interrogation Critical / Major
- Review Critical / Major
- Facts / Boundary

このRoundで修正が必要になった場合、修正後にもう一度最終Roundを実行します。

## Completion

以下をすべて満たすまで完了としません。

- Interrogation Critical = 0
- Interrogation Major = 0
- Review Critical = 0
- Review Major = 0
- Official Specification Coverage MatrixのCritical / MajorにPartial / Missingが0
- Reader Question Coverage MatrixのOverview範囲のCritical / MajorにPartial / Missingが0
- 主要Concept / Evidenceについて「何が分かるか・何は分からないか・どの判断に使うか」を必要な範囲で説明できる
- 名称・例・Fieldの列挙だけで終わる主要Sectionがない
- 主要な複雑関係が適切なMarkdown / Mermaidで外部化されている
- Term / Concept LedgerのCritical / Majorな未解決語が0
- `Needs Toggle = Yes`かつ`Toggle Status = Missing`が0
- 補足が必要な用語が外部検索なしで理解できる
- 重要な前提やRequirementをトグルだけへ隠していない
- Out of Overview判定に明示的な理由がある
- Review修正後の必要な再Interrogationが完了している
- 必要な再Reviewが完了している
- **変更なし最終Roundを1回通過している**

この条件を満たす前に「完成」、「抜け漏れなし」と宣言してはいけません。

## 保存

成果物はMarkdownノートです。
既存ノート更新では特別な理由がなければURLとIDを維持します。

新規作成または意味のある更新を保存する直前に、`.codex/skills/COMMON.md`の更新日時ルールに従いFront Matterの`reviewed_at`を現在の日本時間`YYYY-MM-DD HH:MM JST`へ更新します。
読者に意味のある変更では`_data/article_changes.yml`も更新し、Entryの`date`も`YYYY-MM-DD HH:MM JST`まで記録します。