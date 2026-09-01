---
name: official-docs-router
description: 指定技術と採用する関連技術をDiscovery Frontierで固定点まで一次Source探索し、各Source内部を再帰的にUnknown Artifact / Topic = 0までInventoryし、Evidence・Version / Status・Coverageを指摘ゼロまで反復監査してから、ユーザー承認後にOverview / Mechanism SkillへRoutingする。
---

# Official Docs Router

このSkillは、指定技術・Protocol・Productについて、Source Discovery、関連技術Closure、Source内部Inventory、Semantic Inventory、Evidence Consistency、情報取捨選択、重複統合、階層構造設計を独立したGateとして扱うOrchestratorです。

目的は公式サイトをそのまま複製することではありません。
対象技術を正しく理解するために必要・有用な情報を残し、不要であることを具体的に説明できるものだけを除外します。迷う場合はKeepを優先します。

同じ内容は可能な限り1つのNoteへ統合しますが、Source固有情報、異なるSpecification Family、Version差分、Status差分を失ってはいけません。

## 最優先ルール

最初に必ず次を読みます。

- `.codex/skills/COMMON.md`
- `.codex/skills/MARKDOWN.md`
- `.codex/skills/overview-note/SKILL.md`
- `.codex/skills/overview-interrogate/SKILL.md`
- `.codex/skills/overview-review/SKILL.md`
- `.codex/skills/mechanism-note/SKILL.md`
- `.codex/skills/mechanism-interrogate/SKILL.md`
- `.codex/skills/mechanism-review/SKILL.md`
- `docs/authoring-workflow.md`

公式資料にない事実を公式記載のように扱ってはいけません。

**Human Approval Gateは必須です。構成提案を提示したTurnで必ず停止し、ユーザー承認前にDirectory / Note作成や本文執筆を開始してはいけません。**

**Pruning DefaultはKeepです。Excludeには具体的根拠とCoverage先が必要です。**

**Source Discoveryは最低3 Round必須です。最低3 RoundかつDiscovery Closure条件をすべて満たすまで終了してはいけません。**

**関連技術・Binding・Standard・Implementerを最終Treeで独立Note化または主要Mechanismとして採用する場合、その対象を`Discovery Frontier`へ昇格し、その対象自身のPrimary Sourceを探索しなければいけません。記事だけを根拠に関連技術Noteを作ってはいけません。**

**Source内部InventoryはTop-level分類だけでは完了しません。採用候補Artifactは再帰的に確認し、`Unknown Page / Artifact / Topic = 0`になるまで終了してはいけません。**

**Sourceの記述と実体Tree / Schema / Sample / Version / Statusを必ず相互照合します。矛盾や不一致を未解決のまま構成提案へ進んではいけません。**

**Selection Audit、Evidence Consistency Audit、Structure Auditは回数上限を設けません。新規指摘が0になるまで反復します。**

**後工程で新しい重要Source / Related Target / Artifact / Topicが見つかった場合、現在の下流Gate合格結果はすべて無効です。必ずDiscoveryへ戻り、Closureから再実行します。**

**ユーザー向けの構成作成・構成提案・Directory名・Note名・監査結果説明は日本語を既定とします。英語だけの見出しやNote名を安易に作らず、固有名詞・Protocol名・Version名・RFC名・Schema/API識別子など原文維持が必要な語だけ英語のまま残します。**

## ユーザー向け出力言語

ユーザーが別言語を明示しない限り、構成設計と提案は日本語で行います。

### 日本語にするもの

- ユーザーへ見せる監査Summaryの見出しと説明。
- Directory名。
- Note名。
- Noteの役割説明。
- 採用理由、除外理由、Merge理由、Version / Status上の注意点。
- Human Approval Gateで提示する階層Tree。
- 承認後に実装するDirectory / Noteの表示Title。

### 原文を維持するもの

- AP2、UCP、A2A、MCP、x402などの正式Protocol / Product名。
- RFC / Internet-Draft / Standard名。
- GitHub Repository名、Package名、Module名。
- API、Schema、Field、Header、Capability URIなどの識別子。
- `Overview` / `Mechanism`などSkill内部Routing Label。

### Note名の作り方

Note名は**日本語の説明語 + 必要な固有名詞**を基本にします。

良い例:

```text
AP2の全体像と現在地 [Overview]
AP2 v0.2のプロトコルモデルと検証責務 [Mechanism]
Agent Authorization Frameworkの仕組み [Mechanism]
Checkout MandateとCheckout Receipt [Mechanism]
セキュリティとプライバシー [Mechanism]
AP2・A2A・MCP・UCPの役割と現在の接続状況 [Overview]
UCP AP2 Mandates Extensionの仕組み [Mechanism]
AP2とx402 [Mechanism]
FIDO Alliance移管と標準化の現在地 [Overview]
AP2とVerifiable Intent [Mechanism]
```

避ける例:

```text
Protocol Integration
Security and Privacy
Implementation Considerations
Evolution & Standardization
SDK & Reference Implementation
```

公式文書名を示す必要がある場合でも、ユーザー向けNote名は日本語で責務が分かる形を優先し、Source欄で正式Titleを保持します。

内部Audit TableのField名や固定Status値は英語でも構いませんが、ユーザーへ説明する時は意味を日本語で補います。

## 1. Targetを確定する

対象技術について次を記録します。

- 正式名称。
- Alias / 略称。
- Versionまたは確認日。
- Learn上の配置先。
- 既存Note。
- ユーザー指定Seed URL。

略称だけで探索せず、正式名称とAliasの両方をSearch Termに使います。

最初のTargetを`Discovery Frontier`へ登録します。

| Target | Relation | Why in Scope | Frontier Status |
|---|---|---|---|
| `<main target>` | Root | User target | Pending |

## 2. 必須Source Categoryを定義する

各Discovery TargetについてPage探索より先にSource Inventoryを作ります。
次のCategoryは原則すべて確認します。存在しない場合も`Not Found`または`N/A`として証跡を残します。

### A. Official Documentation

最優先Critical Categoryです。

- Official Documentation Site。
- Developer Documentation。
- 別Domain / Subdomain。
- Versioned Documentation。
- Reference Documentation。

### B. Official Specification / Standards

Critical Categoryです。

- Normative Specification。
- Protocol Specification。
- Schema / Data Model。
- Extension Specification。
- Binding / Transport Specification。
- Standards BodyへContribution / Transferされた仕様。

### C. Official GitHub / Source Repository

Critical Categoryです。

- Official Organization。
- Main Repository。
- Related Repository。
- Integration / Extension Repository。
- SDK / Sample / Demo Repository。

### D. Official Blog / Engineering / Announcement

- Launch Announcement。
- Engineering Blog。
- Protocol Design / Architecture記事。
- Integration記事。
- Version Update記事。
- 対象技術Tag / Category / Search結果。

### E. Official Guides / Tutorials / Samples

- Quickstart / Getting Started。
- Integration Guide。
- SDK Guide。
- Reference Implementation。
- Samples / Examples / Scenario。

### F. Ecosystem / Community Documentation

- ユーザー指定Source。
- 公式Sourceから参照されるCommunity Documentation。
- 独自Specificationを持つEcosystem Site。
- 対象技術名を冠する主要Documentation Site。

CommunityというAuthorityだけを理由に除外してはいけません。

### G. Standardization / Governance

- Standards Body。
- Working Group。
- Contribution / Transfer。
- Governance Repository。
- 後継仕様 / 関連Trust Framework。

### H. Release / Changelog

存在確認は必須です。
Note化は重要なVersion差分がある場合だけです。

### I. Ecosystem Implementers / Providers

対象技術を実際に採用・統合する主要事業者の一次資料を確認します。

- Payment Provider / NetworkのDeveloper Documentation。
- Wallet / Credential Providerの技術資料。
- Maintainerが公式に挙げるPartner Integration。
- Protocol固有の実装・Trust Model・Integration情報を持つ資料。

単なるPartner一覧やMarketing記事は採用しません。

## 3. Discovery Round 1 — Category Sweep

必須Categoryを広く埋めます。
各Frontier Targetについて正式名称とAliasで最低限次のQuery Patternを使います。

```text
"<正式名称>" documentation
"<正式名称>" docs
"<正式名称>" specification
"<正式名称>" protocol specification
"<正式名称>" GitHub
"<正式名称>" blog
"<正式名称>" engineering
"<正式名称>" quickstart
"<正式名称>" examples
"<正式名称>" integration
"<正式名称>" extension
"<正式名称>" standard
"<正式名称>" payment provider
"<正式名称>" wallet
"<Alias>" documentation
"<Alias>" specification
"<Alias>" GitHub
```

Round 1ではSource候補を広く集め、強くPruneしません。

## 4. Discovery Round 2 — Link Graph / Repository / Organization Sweep

Round 1で見つけたSource同士のLink Graphを辿ります。

最低限次を確認します。

- Documentation → Repository。
- Repository README / mkdocs / docs config → Documentation Domain。
- Documentation → Specification / Extension / Integration。
- Documentation → 別Domain / Subdomain。
- Blog → Specification / Repository。
- Resources / Related Links → 技術Source。
- Standards Body → Contribution元 / 後継仕様。
- Main Repository → Related Repository / Sample Repository。
- Official GitHub Organization → 同技術名・Integration名を持つRelated Repository。
- Samples → Integration対象Protocol / Provider。

## 5. Discovery Round 3 — Adversarial Missing-source Search

既知Sourceの再発見ではなく、Inventoryにない重要Sourceを探すRoundです。

最低限次を問い直します。

- 別の公式Documentation Domainはないか。
- 同名Protocolの別Specification Siteはないか。
- Integration / Extension専用SiteやRepositoryはないか。
- Standards Body側に追加技術資料はないか。
- Provider / Wallet側に実装資料はないか。
- Maintainer以外の公式Engineering記事はないか。
- Version移管前後でSource Domainが変わっていないか。
- 関連技術を説明する記事のリンク先に、その技術自身のSpecification / Repositoryがないか。

Discovery中に見つかった重要Keywordも組み合わせます。

## 6. Discovery Frontier Expansion — 関連技術を固定点まで展開する

Discovery中または後工程で、次のいずれかに該当するRelated Targetを見つけたら`Discovery Frontier`へ追加します。

### Frontierへ昇格する条件

- 最終Treeで独立Note化する予定。
- Main Targetの重要Mechanismを定義する独立Specification / Binding / Extension。
- StandardizationでMain Targetと並んで候補基盤・後継仕様として扱われる。
- Main TargetとのIntegration仕様を独自に定義する。
- Main TargetのSecurity / Trust Modelを補完する別仕様。
- Main Targetの現行Statusを理解する上で不可欠なImplementer固有仕様。

### Frontierへ昇格しないもの

- 単なるPartner名。
- Marketing上のMentionだけ。
- Main Targetを利用しているだけで独自Mechanismを持たない事例。
- 一般的な比較記事。

Frontierへ昇格したTargetは、Main Targetと同様に最低限以下を確認します。

- Official Documentation。
- Specification。
- Official Repository。
- Version / Status。
- Main Targetとの関係を示す一次Evidence。

例えば`AP2とVerifiable Intent`を独立Note化するなら、Mastercard/FIDOの記事だけでは不足です。Verifiable Intent自身のSpecification、Documentation、Repository、Version / Statusを取得するまでFrontierはClosedになりません。

## 7. Name Collision / Lineage Audit — 同名別技術を分離する

Main Targetと各Frontier Targetについて、同名・類似名の別Protocol / Productを意図的に検索します。

最低限次を比較します。

- Maintainer / Organization。
- Canonical Domain。
- Repository Owner。
- Specification Lineage。
- Role Model。
- Data Model / Wire Model。
- Version history。

同名でもLineageが異なる場合は別Targetとして明示し、Main Targetへ混入させてはいけません。

除外する場合もSource Inventoryに残します。

```text
Relation: Name Collision / Different Protocol
Adopt: No
Exclusion Reason: lineage / role model / data model / wire modelが異なる
Covered By: N/A — 別Protocol
```

`Unresolved Name Collision = 0`が必須です。

## 8. Discovery Round 4+ — Frontier変化がある限り続ける

最低3 Roundは必須です。

新しい重要Sourceまたは新しいFrontier Targetが1件でも見つかった場合、追加Roundを実行します。

新しいFrontier Targetを追加した場合、そのTargetのCategory Sweep / Link Graph / Adversarial Searchを最低限実行してからClosure判定へ戻ります。

各Roundを記録します。

| Round | Focus | New Important Sources | New Frontier Targets | Notes |
|---|---|---:|---:|---|
| 1 | Category Sweep | | | |
| 2 | Link Graph / Repository | | | |
| 3 | Adversarial Missing-source | | | |
| 4+ | Follow-up / Frontier Expansion | | | |

## 9. Discovery Closure Gate — 2回連続ゼロで固定点を確認する

Discoveryを1回の`New important sources = 0`だけで閉じてはいけません。

最後に**異なる探索戦略で2回連続Closure Round**を行います。

### Closure Round A — External Search Closure

- Search EngineでCategory別再検索。
- 正式名称 / Alias / Integration Keywordの組み合わせ。
- `specification` / `GitHub` / `standard` / `extension` / `provider`を再検索。
- Name Collision検索。

### Closure Round B — Graph / Repository Closure

- 全Adopt SourceのOutbound Link再走査。
- Official Organizationの関連Repository再確認。
- Docs Config / README / Resources / Standards Body Link再確認。
- 全Frontier TargetのPrimary Source確認。

完了条件は以下を**すべて**満たすことです。

- Discovery Round >= 3。
- Closure Round AのNew Important Sources = 0。
- Closure Round AのNew Frontier Targets = 0。
- Closure Round BのNew Important Sources = 0。
- Closure Round BのNew Frontier Targets = 0。
- Unexpanded Frontier Target = 0。
- Unresolved Name Collision = 0。
- Source Category Unknown = 0。
- Critical Category未確認 = 0。

## 10. Global Reset Rule — 後工程で新Sourceを見つけたらDiscoveryへ戻る

Inventory、Consistency、Selection、Structure、Final Auditのどこであっても、以下が見つかった場合はDiscovery Closureが崩れたとみなします。

- 新しい重要Source。
- 新しいFrontier Target。
- 未探索のSpecification / Repository。
- 新しいName Collision。
- 現行理解を変えるVersion / Status差分。

その場合は以下を行います。

1. 新Source / TargetをSource Inventory / Discovery Frontierへ追加する。
2. `Discovery Closed = false`に戻す。
3. 下流の`Inventory Audit = 0`、`Consistency = 0`、`Selection = 0`、`Structure = 0`、`Final Audit = 0`をすべて無効化する。
4. Discovery Closure Gateから再実行する。
5. Source内部Inventory以降も再実行する。

**後工程で見つけたSourceをその場で追加して、既存の「指摘0」を維持してはいけません。**

## 11. Authorityを分類する

- Normative / Standards Body。
- Official / Maintainer。
- Official Repository。
- Official Blog / Announcement。
- Ecosystem Implementer。
- Community / Ecosystem。
- Third-party。

AuthorityはMetadataであり、自動除外Filterではありません。

## 12. Source Internal Inventory — Source内部を完全に列挙する

Discovery Closure後、各Sourceの内部Page / Artifactを列挙します。

### Documentation Site

最低限次を確認します。

- Header Navigation。
- Sidebar。
- Mobile Navigation。
- Index Page。
- Footer内の技術Link。
- Version Selector。
- Sitemap / RSS / llms.txtがあれば補助利用。
- 別Domain / Subdomainへの技術Link。

`Unknown URL / Section = 0`まで確認します。

### Specification Site

最低限次を確認します。

- Specification Index。
- TOC。
- Extension / Binding / Security / Appendix。
- Version別仕様。
- Normative / Non-normativeの区別。

`Unknown Spec Artifact = 0`まで確認します。

### GitHub Repository

**Root Treeの全Top-level Directory / 主要Fileを一度必ず列挙します。既知Directory名だけを拾ってはいけません。**

最低限次を分類します。

- `docs` / `spec` / `specs` / `schema` / `schemas`。
- `sdk` / `src` / `lib`。
- `samples` / `examples` / `scenarios`。
- `web-client` / `client` / `demo` / `app`。
- `tools` / `cli`。
- `extensions` / `integrations` / `bindings`。
- README / mkdocs / package metadata / build config。
- Unknown nameのTop-level Directory。

Unknown Directoryは中身を確認して`Adopt Candidate / Exclude Candidate / Infrastructure`へ分類します。

READMEやDocs設定に記載されているArtifactとRoot Treeを照合し、片方にしか存在しないArtifactがないか確認します。

### Blog / Engineering Site

- 対象技術Tag / Category。
- Archive。
- Pagination。
- Search結果。
- Launch / Architecture / Integration / Version Update記事。

`Unreviewed relevant article = 0`まで確認します。

### Samples / Guides

- Scenario一覧。
- Language別実装。
- Provider別実装。
- Protocol別Integration。
- Demo / Web Client。

`Unknown Sample / Guide = 0`まで確認します。

## 13. Recursive Semantic Inventory — 採用候補Artifactを中身まで再帰確認する

Top-level Directoryを分類しただけでInventory完了としてはいけません。

`Adopt Candidate`または技術的意味を持つArtifactについて、学習上の責務が分かる粒度まで再帰的に降ります。

例えばRepositoryなら次を確認します。

```text
sdk/
├─ models/
├─ schemas/
│  ├─ protocol/
│  └─ integration/
├─ runtime/
│  ├─ validation
│  ├─ chain verification
│  ├─ constraints
│  └─ signature / credential
└─ tests/
```

次を必ず抽出します。

- Data Model / Schema。
- Runtime Mechanism。
- Validation / Verification。
- Constraint / Policy。
- Signature / Credential / Privacy機構。
- Receipt / Evidence / Error Model。
- Integration-specific Schema / Type。
- Scenario / Language / Provider差分。
- Demo / Clientが実際に何をExerciseするか。

単なるFile列挙で終わらず、各Artifactの`Purpose`と`Content Topics`を持ちます。

**再帰停止条件は、下位Artifactを見ても新しい学習Topicが増えないことを説明できることです。**

`Unknown Semantic Topic = 0`になるまで続けます。

## 14. Internal Inventory Audit Loop — Unknown = 0まで反復

Source内部InventoryとRecursive Semantic Inventory後、独立Auditを行います。

最低限次を確認します。

- Root / Navigationに存在するが未分類のArtifactがないか。
- READMEで説明されているがInventoryにないArtifactがないか。
- Docs NavigationとRepository Treeの差分がないか。
- Web Client / Demo / Tooling等を名前だけで見落としていないか。
- Blog Archiveで未評価記事がないか。
- Specification Indexに未確認Extension / Appendixがないか。
- Samplesで未確認Scenario / Language / Providerがないか。
- SDK / Schema / Runtime内部に未確認の技術責務がないか。
- Integration用SchemaやTypeをCore Artifactに隠していないか。

指摘が1件でもあればInventoryへ戻ります。

**完了条件は全採用候補Sourceで`Unknown Page / Artifact / Semantic Topic = 0`かつ、1 Audit Roundの新規指摘 = 0です。**

| Inventory Audit Round | Unknown Pages | Unknown Artifacts | Unknown Topics | Missing Links | New Findings |
|---|---:|---:|---:|---:|---:|
| 1 | | | | | |
| 2 | | | | | |

新しいSource / Frontier Targetが見つかった場合はSelectionへ進まず、Global Reset Ruleを適用します。

## 15. Evidence Consistency Audit Loop — Sourceの主張と実体を突き合わせる

Inventory完了後、Sourceに書かれているClaimと実際のEvidenceを相互照合します。

### Claim ↔ Artifact Audit

最低限次を突き合わせます。

- READMEに書かれたPath ↔ 現在のRepository Tree。
- Documentation Navigation ↔ 実在Page。
- Specificationが挙げるSchema ↔ 実Schema File。
- Sample一覧 ↔ 実Scenario Tree。
- SDK説明 ↔ 実Runtime Module。
- Integration説明 ↔ 実Extension / Binding / Schema。

片方にしか存在しない場合は`Consistency Issue`として記録します。

### Version / Status Audit

各重要Source / Artifact / IntegrationについてStatusを記録します。

- Current / Stable。
- Draft。
- Alpha / Beta / Experimental。
- Planned / Coming Soon。
- Deprecated / Historical。
- Unknown。

`Unknown`は解消します。

特に次を禁止します。

- `coming soon`を実装済みとして扱う。
- `alpha`を現行Stable仕様として扱う。
- v0.1のBindingをv0.2のCanonical Bindingとして扱う。
- DraftをNormative Standardとして扱う。

### Contradiction Resolution

Source間や同一Source内で矛盾した場合は次を行います。

1. 実体Tree / 現在のCanonical Artifactを確認する。
2. Version / 更新時点を確認する。
3. Normative / Maintainer / RepositoryのAuthorityを比較する。
4. どちらを本文で採用するかと理由を記録する。
5. 古い情報も学習価値があればHistoricalとして保持する。
6. 未解決Upstream Issueなら「未解決」であること自体をStatusとして保持する。

**Consistency Issueが1件でもあれば修正・再Inventoryし、Evidence Consistency Auditを最初からやり直します。**

完了条件は以下です。

- Unresolved Claim / Artifact Mismatch = 0。
- Unknown Version / Status = 0。
- Unresolved Contradiction = 0。ただしUpstreamで未解決と確認できたIssueは`Known Open Conflict`として解決済み分類できる。
- 1 Audit RoundのNew Consistency Findings = 0。

新しいSource / Frontier Targetが見つかった場合はGlobal Reset Ruleを適用します。

## 16. Source単位で採用・除外する

Source候補を`Adopt / Exclude / Pending`で評価します。

### Adopt

次のどれかに該当すれば原則Adoptします。

- Concept、Architecture、Protocol、Flow、API、Security、Integration、Use Case、設計背景を理解する情報がある。
- 独自仕様・独自実装・独自Trust Modelがある。
- 他Sourceとの差分が学習上有用。
- ユーザー指定Source内に学習価値のあるPageがある。

### Exclude

Source全体のExcludeは全体確認後に次を証明できる場合だけです。

- 対象技術と無関係。
- 全PageがDuplicate / Redirect / Alias。
- 技術・概念理解に寄与する情報がない。
- Legal / Company / Contact情報だけ。
- Name CollisionでMain Targetとは別Protocolである。

## 17. Page / Artifact単位で一次選抜する

各Page / Artifactに`Adopt / Exclude / Pending`を設定します。

Pruning DefaultはKeepです。

Exclude時は必ず次を記録します。

- `Exclusion Reason`。
- `Covered By`。

Covered Byを説明できない場合はKeepします。
Name Collisionなど別ProtocolでCoverage不要な場合は`Covered By: N/A — out of lineage`を許可します。

## 18. Page / Artifact / Topic Inventoryを作る

最低限次を保持します。

| Field | 内容 |
|---|---|
| Title / Artifact | 公式TitleまたはArtifact名 |
| Canonical URL / Path | 正規URLまたはRepository Path |
| Source | 所属Source |
| Discovery Target | Main / Related Target |
| Relation to Main | Core / Integration / Standardization / Implementer / Historical / Collision等 |
| Authority | Authority |
| Version | Version / Date |
| Status | Stable / Draft / Alpha / Planned / Historical等 |
| Parent Section | 親Section |
| Purpose | 中心的説明責任 |
| Adopt | Yes / No / Pending |
| Exclusion Reason | 除外理由 |
| Covered By | Coverage先 |
| Content Topics | 内容Topic |
| Merge Group | 統合候補 |
| Route | Overview / Mechanism / Pending |
| Dependency | 前提Note |
| Evidence | Claimを裏付けるPage / Path |

Pendingが残っている状態ではClusteringへ進みません。

## 19. Content Clustering / Merge Draft

同じ内容をSource横断でCluster化します。

### Merge候補

- 中心質問が同じ。
- 同じConcept / Flow / Mechanismを別表現で説明する。
- 一方が他方の要約で独自情報がほぼない。
- 同一Specificationの別Format。

### Separate候補

- 中心質問が異なる。
- 独自Data Model / Flow / Security / Integration / 設計背景がある。
- 別Specification FamilyでProtocol構造が異なる。
- Version / Statusが異なり、同一Noteにすると現行状態を誤解させる。
- Related Target自身のMechanismが独立しており、Main Targetの補足だけでは表現できない。

Mergeは削除ではありません。統合元の独自情報を失ってはいけません。

Merge GroupごとにPrimary SourceとSupporting Sourceを決めます。

## 20. Coverage Contractを作る

各Adopt Source / Page / Artifact / Semantic Topicが、最終的にどのNoteのどの責務でCoverageされるかを明示します。

最低限次を保持します。

| Adopt Item / Topic | Destination Note | Coverage Responsibility | Primary / Supporting | Status |
|---|---|---|---|---|
| | | | | Covered / Missing |

次を禁止します。

- `SDK Noteに入れる`だけで内部Runtime機構のCoverageを省略する。
- `Integration Noteに入れる`だけでSchema / Status / Binding差分を省略する。
- `Specification Noteに入れる`だけで独立Data Artifactを落とす。
- `関連技術Noteに入れる`のに、その関連技術自身のPrimary Sourceを持たない。

**Adopt ItemだけでなくSemantic Topic単位でCoverageを確認します。**

`Coverage Status = Missing`が1件でもあればSelection Auditへ進めません。

## 21. Selection Audit Loop — 指摘ゼロまで無制限反復

Source / Page / Artifact選抜、Merge Draft、Coverage Contractを監査します。

### Missing Audit

- 採用Source内に未Inventory Page / Artifact / Topicがないか。
- 必要PageをExcludeしていないか。
- ExcludeしたPageに独自情報が残っていないか。
- Blog / FAQ / Glossary / Resource / Demoから重要Topicを落としていないか。
- Schema / SDK Runtime / Integration Statusを落としていないか。
- 独立Note化するRelated TargetのPrimary Sourceが欠けていないか。
- Implementerを採用するなら、単なる発表だけでなく固有技術資料の有無を確認したか。

### Wrong Exclusion Audit

- Authorityが低いだけで落としていないか。
- Covered Byが実際には内容をCoverageしていないPageがないか。
- Marketingに見えるが技術的独自情報を含むPageがないか。
- Demo / Web ClientをUIだけと判断して誤除外していないか。

### Wrong Inclusion Audit

- 技術理解を増やさないPageをKeepしていないか。
- 同じ情報だけを繰り返すBlog / Announcementを独立Note化していないか。
- Partner一覧 / Company情報を混ぜていないか。
- Name Collisionの別Protocolを混ぜていないか。

### Merge Audit

- 同じ内容を複数Noteへ残していないか。
- Source横断の重複を見落としていないか。
- 異なるSpecification Familyを誤Mergeしていないか。
- Version / Statusが異なるものを誤って同一現行仕様としてMergeしていないか。
- MergeによってSource固有情報が消えていないか。

### Coverage Audit

- 各ExcludeにExclusion ReasonとCovered ByまたはN/A理由があるか。
- 各Adopt Item / Topicが最終NoteのどこでCoverageされるか説明できるか。
- Schema、Runtime、Flow、Status、Version差分がCoverage Contractに載っているか。
- Related TargetのPrimary Sourceを説明できるか。
- Pending = 0か。

指摘が1件でもあればInventory / Consistency / Adopt / Exclude / Merge / Coverage Contractを修正し、Selection Auditを最初から再実行します。

**Selection Audit完了条件は1 Round全体で新規指摘が0件になることです。回数上限はありません。**

新しいSource / Frontier Targetが見つかった場合はGlobal Reset Ruleを適用します。

## 22. Information Architectureを設計する

Selection Audit完了後に初めて階層化します。

Navigation、Specification TOC、技術的依存関係、Source Family、Version / Statusを参考にしつつ、選抜・統合後のNote群をLearn向けに整理します。

**Information ArchitectureのDirectory名・Note名は日本語を既定とします。**

- `Canonical AP2 v0.2`のような固有名詞中心の分類名は必要に応じて残してよい。
- 一般概念の分類は`Protocol Integration`ではなく`プロトコル連携`、`Evolution & Standardization`ではなく`進化と標準化`のように日本語化します。
- Note名は「何を学ぶNoteか」が日本語で分かる名前にします。
- 公式文書名をそのままNote名にする必要はありません。正式TitleはSource Metadataで保持します。
- `[Overview]` / `[Mechanism]`はRouting Labelなのでそのまま残します。

## 23. Structure Audit Loop — 指摘ゼロまで反復

Proposed Treeについて次を監査します。

- 必要NoteがTreeから落ちていないか。
- 同じ内容のNoteが複数存在しないか。
- Directoryが深すぎないか。
- Flatすぎて意味分類を失っていないか。
- Source Family境界を壊していないか。
- CurrentとHistorical / Draftを誤認させる構造になっていないか。
- Overview → Mechanism Dependencyが自然か。
- SDK / Samples / Integration / Standardizationの位置が自然か。
- Coverage ContractのDestination NoteがすべてTreeに存在するか。
- 独立Related Target NoteがあるのにPrimary Source不在になっていないか。
- ユーザー向けDirectory / Note名が日本語中心になっているか。
- 英語のみの一般概念Titleが残る場合、原文維持が必要な理由を説明できるか。

指摘があればTreeを修正し、Coverage Contractも更新して再監査します。

**`New structure findings = 0`で完了です。**

新しいSource / Frontier Targetが見つかった場合はGlobal Reset Ruleを適用します。

## 24. Proposal前Final Audit — Source↔Treeを双方向に検査する

構成提案直前にTreeからSourceへ逆向きに監査します。

各Noteについて次を確認します。

- このNoteの存在理由は何か。
- Primary Sourceは何か。
- Supporting Sourceは何か。
- Related Target Noteなら、そのTarget自身のPrimary Sourceを持つか。
- Coverageする全Semantic Topicは何か。
- Version / Statusを誤解させないか。
- Noteから辿れないAdopt Itemが残っていないか。
- Note名が日本語で学習責務を表現しているか。

さらにSource側からTreeへ正向きに再確認します。

- Adopt Source / Artifact / TopicがすべてTree上のNoteへ到達するか。
- Exclude ItemはすべてCovered Byまたは明確な不要理由を持つか。
- Discovery FrontierのTargetがすべてClosedになっているか。
- Name CollisionがすべてResolvedになっているか。

**Forward Coverage Missing = 0、Reverse Orphan Note = 0、Unclosed Frontier = 0、Unresolved Collision = 0、New Findings = 0になるまで反復します。**

新しいSource / Frontier Targetが見つかった場合はGlobal Reset Ruleを適用し、Proposal前Final Auditだけを局所的に続けてはいけません。

## 25. Directory / Note構成を日本語で提案し、必ず停止する

ユーザー向け提案は日本語で提示します。内部Gate名を英語で保持していても、ユーザーへ見せる見出しと説明は日本語にします。

提示順は次です。

1. 探索ラウンドの概要。
2. 関連技術探索とDiscovery Closureの結果。
3. Source探索カバレッジ。
4. 同名別Protocol / Lineage確認結果。
5. Source内部Inventory監査結果。
6. Evidence整合性監査結果。
7. 採用・除外・Merge監査結果。
8. 採用Source。
9. 主な除外SourceとCoverage先。
10. Merge方針。
11. Version / Status上の注意点。
12. 日本語の階層Directory Tree。
13. 各Noteの`[Overview]` / `[Mechanism]`。
14. ユーザーへの承認確認。

Treeは次を基本形にします。

```text
📁 <技術名> 公式・関連情報 日本語ノート
├─ <技術名>の全体像と現在地 [Overview]
├─ 📁 <日本語の大分類>
│  ├─ <日本語のNote名> [Overview]
│  ├─ <日本語のNote名> [Mechanism]
│  └─ 📁 <日本語の下位分類>
│     └─ <日本語のNote名> [Mechanism]
└─ 📁 <独立Specification Family名>
   └─ <日本語のNote名> [Mechanism]
```

例えばAP2なら、以下のような日本語中心の構成を優先します。

```text
📁 AP2 公式・関連情報 日本語ノート
├─ AP2の全体像と現在地 [Overview]
├─ 📁 Canonical AP2 v0.2
│  ├─ AP2 v0.2のプロトコルモデルと検証責務 [Mechanism]
│  ├─ Agent Authorization Frameworkの仕組み [Mechanism]
│  ├─ Human Present / Human Not Presentの取引フロー [Mechanism]
│  ├─ Checkout MandateとCheckout Receipt [Mechanism]
│  ├─ Payment MandateとPayment Receipt [Mechanism]
│  ├─ セキュリティとプライバシー [Mechanism]
│  └─ 実装時の考慮事項 [Mechanism]
├─ 📁 プロトコル連携
│  ├─ AP2・A2A・MCP・UCPの役割と現在の接続状況 [Overview]
│  ├─ UCP AP2 Mandates Extensionの仕組み [Mechanism]
│  └─ AP2とx402 [Mechanism]
├─ 📁 SDKとリファレンス実装
│  └─ AP2 Python SDK・Canonical Schema・Reference Architecture [Mechanism]
└─ 📁 進化と標準化
   ├─ AP2 v0.1からv0.2への変化 [Overview]
   ├─ FIDO Alliance移管と標準化の現在地 [Overview]
   └─ AP2とVerifiable Intent [Mechanism]
```

構成提案を提示したTurnでは必ず停止します。

## 25.5 承認済みTreeをBuild Manifestへ固定する

ユーザーがTreeを承認した直後、Note本文を書き始める前に、承認済みDirectory / Noteを`.codex/research-runs/<target>.json`へ保存します。
**会話の記憶だけを進捗管理に使ってはいけません。**

Manifestの各Itemは最低限次を持ちます。

| Field | 内容 |
|---|---|
| id | Directory / Note ID |
| kind | Directory / Note |
| sourcePath | 作成するSource Markdown Path |
| title | 承認された表示Title |
| directoryId | 承認された親Directory |
| permalink | 固定するURL |
| route | Overview / Mechanism |
| stage | pending / writing / interrogating / reviewing / needs_revalidation / blocked / done |
| attempts | Writing再開回数 |

承認時点ではItemを`pending`にします。
作業開始前に`writing`、Interrogate前に`interrogating`、Review前に`reviewing`、No-change Roundまで完了して実ファイルとの一致を確認した後だけ`done`へ進めます。

### 途中停止からの自動Recovery

同じTargetを再開する時は、Discoveryや構成作成を最初からやり直す前にManifestを確認します。

```bash
python3 scripts/research-manifest.py resume .codex/research-runs/<target>.json
```

`stage != done`の最初のItemをRecovery Pointとし、そのStageを**冪等に最初から再実行**します。
`writing`の途中で停止した場合はDraftが部分的に存在しても再読込して完成させます。
`interrogating` / `reviewing`の途中なら、そのNote全文を再評価してStageを再実行します。

新しい重要Source / Frontier Targetが見つかった場合は通常どおりGlobal Reset Ruleを適用し、影響する`done` Itemを`needs_revalidation`へ戻します。Manifest自体を捨てて既完了Noteを忘れてはいけません。

各CheckpointはRepositoryへ保存します。長いResearchで一度のTurnに全Noteを完成できなくても、次回はManifestから続行できます。

## 26. ユーザー承認後のPre-build Interrogation

承認後、実装前にもう一度確認します。

- Discovery最低3 Roundを本当に通したか。
- Closure Round A / Bが両方0か。
- Discovery FrontierのUnexpanded / Unclosed Target = 0か。
- Unresolved Name Collision = 0か。
- Source内部Unknown Page / Artifact / Topic = 0か。
- Evidence Consistency Issue = 0か。
- Unknown Version / Status = 0か。
- Coverage Contract Missing = 0か。
- Selection Audit新規指摘 = 0か。
- Structure Audit新規指摘 = 0か。
- Proposal前Final Audit新規指摘 = 0か。
- 必要情報を削りすぎていないか。
- ExcludeすべてにCovered Byまたは明確な不要理由があるか。
- 承認対象のDirectory / Note名が日本語中心で提示されているか。

新しい重要Source / Frontier Target / Artifact / Topic / Status差分 / Merge候補が見つかった場合はGlobal Reset Ruleを適用します。
承認済みTreeを勝手に変更せず、必要ならTreeを修正してユーザーへ再提案し再承認を取ります。

## 27. Note単位でRoutingする

Routingは統合後のNote単位です。

### Mechanism Route

Data / API / Flow / Validation / State / Security Control / Implementationを追う必要があるNoteは`mechanism-note`へRoutingします。

### Overview Route

Mechanism Routeに該当しない採用Noteは原則`overview-note`へRoutingします。

Routing ConfidenceはHigh / Medium / Lowで保持し、Lowのまま執筆開始しません。

## 28. 各NoteをSub-skillで執筆する

Overview Routeは必ず次を完走します。

1. `overview-note`。
2. `overview-interrogate`。
3. `overview-review`。
4. 修正Round。
5. No-change Round。

Mechanism Routeは必ず次を完走します。

1. Overview Dependency確認。
2. `mechanism-note`。
3. `mechanism-interrogate`。
4. `mechanism-review`。
5. 修正Round。
6. No-change Round。

Router自身が簡易要約で代替してはいけません。

## 29. Directory / Noteを実装する

承認済みTreeに従います。
Nested Directoryは必要な時だけ使います。

**実装時のDirectory名・Noteの表示Titleは、承認された日本語名をそのまま使用します。実装段階で英語Titleへ戻してはいけません。**

File名や内部IDについて既存Project Conventionがある場合はそれに従って構いませんが、ユーザーに表示されるTitleは承認済み日本語名を維持します。

各NoteはPrimary Source、Supporting Source、Coverage Contractを追跡できるようにします。

## 29.5 Post-build Reconciliation — 計画と実装を必ず突合する

全Noteを作成したつもりでも、Manifestと実Sourceを双方向に突き合わせるまで完了扱いにしません。

```bash
python3 scripts/research-manifest.py validate .codex/research-runs/<target>.json
```

最低限次がすべて0である必要があります。

```text
Planned Item Missing = 0
Unexpected Actual Item = 0
Path Mismatch = 0
Parent Directory Mismatch = 0
Title Mismatch = 0
Permalink Mismatch = 0
Stage != done = 0
Overview / Mechanism Note without source <details> = 0
```

特に、Directoryが表示できることや一部Noteが存在することを「構成完成」の代わりにしてはいけません。
**承認済みTreeの全Itemが実在し、正しい親Directoryにあり、Sub-skillのNo-change Roundまで完了して初めてResearch Build完了です。**

Final Coverage Review / Fresh Rediscoveryの後にもReconciliationを再実行します。
新しいNoteが追加された場合はManifestへ追加し、必要ならユーザーへTreeを再提案して承認を取り直します。

## 30. Final Coverage Review / Fresh Rediscovery

完成前にDiscovery Frontier、Closure Round A / B、Recursive Inventory、Evidence Consistency、Coverage Contractを再実行します。

- Critical Source Category Missing = 0。
- Discovery Round >= 3。
- Closure Round A New Important Sources / Targets = 0。
- Closure Round B New Important Sources / Targets = 0。
- Unclosed Frontier Target = 0。
- Unresolved Name Collision = 0。
- Unknown Page / Artifact / Semantic Topic = 0。
- Evidence Consistency Issue = 0。
- Unknown Version / Status = 0。
- Page / Artifact / Topic Pending = 0。
- Coverage Contract Missing = 0。
- Duplicate Note = 0。
- Mergeによる情報欠落 = 0。
- Routing Confidence Low = 0。
- User-visible Directory / Note Titleの日本語化漏れ = 0。
- Critical / Major = 0。

新しい重要Source / Frontier Target / Artifact / Topic / Status差分 / Merge候補が見つかった場合はFailし、Global Reset Ruleを適用します。
必要に応じてTreeを再提案して再承認を取ります。

## Completion

次をすべて満たすまで完了扱いにしません。

- 必須Source Categoryをすべて確認した。
- Discovery Roundを最低3回実行した。
- Closure Round AでNew Important Sources / Frontier Targets = 0。
- Closure Round BでNew Important Sources / Frontier Targets = 0。
- Discovery FrontierのUnexpanded / Unclosed Target = 0。
- Unresolved Name Collision = 0。
- Source Coverage Unknown = 0。
- 全採用候補SourceでUnknown Page / Artifact / Semantic Topic = 0。
- Internal Inventory Auditの新規指摘 = 0。
- Unresolved Claim / Artifact Mismatch = 0。
- Unknown Version / Status = 0。
- Unresolved Contradiction = 0またはKnown Open Conflictとして分類済み。
- Evidence Consistency Auditの新規指摘 = 0。
- Source / Page / Artifact / Topic Pending = 0。
- Coverage Contract Missing = 0。
- Related Target NoteすべてにTarget自身のPrimary Sourceがある。
- Selection Auditの新規指摘 = 0。
- 同一内容のDuplicate Note = 0。
- MergeでSource固有情報を失っていない。
- Structure Auditの新規指摘 = 0。
- Proposal前Final Auditの新規指摘 = 0。
- Forward Coverage Missing = 0。
- Reverse Orphan Note = 0。
- ユーザー向け構成提案が日本語で提示されている。
- 承認されたDirectory / Noteの表示Titleが日本語中心で維持されている。
- 構成提案をユーザーが承認した。
- 技術・仕組みNoteはmechanism-note / interrogate / reviewを完走した。
- それ以外のNoteはoverview-note / interrogate / reviewを完走した。
- Fresh RediscoveryでもClosure Round A / Bが両方0。
- 承認済みTreeのResearch Build ManifestがRepositoryに保存されている。
- Manifestの全Itemが`stage: done`である。
- Planned Item Missing = 0、Unexpected Actual Item = 0。
- Path / Parent Directory / Title / Permalink Mismatch = 0。
- 中断後に再開した場合、ManifestのRecovery Pointから再開し未完了Itemを残していない。
- 最終No-change Roundを通過した。
