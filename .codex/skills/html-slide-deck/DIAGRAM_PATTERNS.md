# Diagram Patterns

この文書は、Composition PatternのRegion内部へ配置する**図そのものの種類**を定義します。
Compositionはページ全体の領域分割、Diagram Patternはその領域の中で関係・順序・境界・差分をどう見せるかを担当します。

まずOWS参照資料から実際に使われている図を抽出し、その後に技術解説で必要になる汎用Patternを追加します。

## OWS参照資料から抽出するDiagram Pattern

### D01 / Many-to-One Hub

複数の呼び出し側が1つの共通入口や中核機能へ収束する図です。
OWSのCLI / SDK / AgentからOWS共通入口へ集約する構成が該当します。

```text
Caller A ─┐
Caller B ─┼──▶ Core / Gateway
Caller C ─┘
```

用途です。

- 共通インターフェース。
- Gateway。
- Broker。
- Aggregator。
- 複数Clientから共通Serviceへの接続。

可変要素です。

- Caller数は2〜4程度。
- Return Flowの有無。
- Core内部を単一Boxにするか、内部Componentを見せるか。

Callerが3つ以上でReturn Flowや内部Componentまで見せる場合は、狭いCompositionへ詰めず全面図を使います。

### D02 / Role Separation

2つ以上の主体の責務分離を見せる図です。
OWSのLLMを提案者、OWSを署名主体とする構成が該当します。

```text
PROPOSER                     SIGNER
┌──────────┐   request   ┌──────────┐
│          │────────────▶│          │
│          │◀────────────│          │
└──────────┘    result   └──────────┘
```

用途です。

- Proposer / Executor。
- Client / Signer。
- Control Plane / Data Plane。
- Human / Agent。

責務名だけではなく、渡すDataと返すResultを矢印Labelで示します。

### D03 / Linear Processing Flow

1つの処理が複数Stepを順番に通る図です。
OWSの署名要求→Policy→復号→署名→結果返却のような処理に使います。

```text
Input → Step 1 → Step 2 → Step 3 → Result
```

用途です。

- Processing Pipeline。
- Validation Flow。
- Build / Verify / Execute。

Step数が多い場合は横1列へ押し込まず、上下2段またはSequenceへ切り替えます。

### D04 / Before / After Architecture

同じSystemが変更前後でどう変化するかを見せます。
OWSの標準署名とOS鍵境界を追加した強化構成が該当します。

```text
BEFORE                       AFTER
┌────────────┐              ┌────────────┐
│ old system │              │ new system │
└────────────┘              └────────────┘
```

用途です。

- 改善前後。
- Migration。
- Security Hardening。
- 新規Layer追加。

Before / Afterで同一要素の位置関係を可能な限り揃え、差分だけを強調します。

### D05 / Two-Problem Concept Diagram

2つの異なる問題をそれぞれ小さな概念図で説明します。
OWSのReachabilityとTrustが該当します。

用途です。

- 根本問題が2つある時。
- 技術問題と運用問題を分けたい時。
- 独立した原因を並べたい時。

左右の図を同じVisual Densityに揃えます。

### D06 / Capability Micro-Visual

機能・特徴ごとに小さな専用図を持たせるPatternです。
OWSのParse / Confirm UI / Origin / Accessの4要素が該当します。

用途です。

- 3〜4個のCapability。
- それぞれを短いVisual Exampleで理解させたい時。

4つすべてを同じ箱＋同じアイコンにせず、各Capabilityの意味に合う小図を使います。

### D07 / Full System Architecture with Boundaries

複数Actor、内部Module、外部Boundaryを一枚の大きな図で見せます。
OWSのSigning Gateway全体像が該当します。

```text
External        System Boundary             Secure Boundary
┌──────┐      ┌──────────────────┐        ┌──────────────┐
│Actor │ ───▶ │ Module / Module  │ ─────▶ │ Secure Asset │
└──────┘      │ Module / Module  │        └──────────────┘
              └──────────────────┘
```

用途です。

- System Architecture。
- Trust Boundary付きArchitecture。
- Platform全体像。

原則として全面図Compositionを使います。

### D08 / Trust Boundary Zones

信頼レベルや責務境界をZoneとして見せます。
OWSのUntrusted / OWS Daemon / Key Boundaryが該当します。

```text
ZONE A        ZONE B                  ZONE C
Untrusted     Controlled System       Secure Boundary
```

用途です。

- Trust Boundary。
- Security Boundary。
- Ownership Boundary。
- Execution Zone。

Zoneの色は装飾ではなく意味を持たせます。

### D09 / Phase Flow

同じSystemでもフェーズによって処理が異なることを見せます。
OWSの接続フェーズと署名フェーズが該当します。

```text
Phase A
A → B → C

Phase B
A → Validate → Confirm → Execute
```

用途です。

- Setup / Runtime。
- Connect / Execute。
- Registration / Transaction。

Phaseごとの頻度や前提条件をLabelで明示します。

### D10 / Sequence Diagram

複数Actor間の通信順序を時系列で見せます。
OWSの署名1回の呼び出し時系列が該当します。

用途です。

- Request / Responseが多い。
- User確認が途中に入る。
- 同じActor間を複数回往復する。

Actorは上部で等間隔に揃え、lifelineも同じx座標で固定します。

### D11 / Alternative Architecture Comparison

採用案と不採用案それぞれを独立した小Architectureとして比較します。
OWSの外部ウォレット案との比較が該当します。

用途です。

- Option A / B。
- Adopt / Reject。
- Centralized / Duplicated。

比較軸を揃え、片方だけ細かく描きません。

### D12 / Timeline / Delayed Execution

時間軸上で「今」と「後で」が異なることを見せます。
OWSの通常txとPermit型署名の違いが該当します。

```text
sign ───────────── execute
      time passes
```

用途です。

- Deferred Execution。
- Expiration。
- Delayed Trigger。
- Async Lifecycle。

### D13 / Layered Defense

複数の独立した防御Layerを積み重ねて見せます。
OWSのPermit型をEndpoint、Policy、Confirm UIの3レイヤで分離する考え方が該当します。

```text
L1 Physical Separation
L2 Policy Separation
L3 Confirmation Separation
```

用途です。

- Defense in Depth。
- Multi-layer Verification。
- Security Controls。

Layer同士が同じ役割に見えないよう、それぞれが防ぐFailureを明示します。

### D14 / Validation Funnel / Policy Filter

入力が複数の条件を順番に通り、許可範囲が狭まっていく図です。
OWSのContract / Function / Argument制限や署名時の再検証に対応します。

```text
Request
  ↓
Contract
  ↓
Function
  ↓
Argument
  ↓
ALLOW / DENY
```

用途です。

- Policy Evaluation。
- Validation Pipeline。
- Authorization Check。

## 技術解説で追加する汎用Diagram Pattern

以下はOWS参照資料だけでは十分に表現されていませんが、AP2など他の技術説明で必要になるため追加します。

### D15 / Data Binding Chain

複数Dataが順番にBindingされ、後続Dataが前段の内容を拘束する関係を見せます。

```text
Data A ──binds──▶ Data B ──authorizes──▶ Data C
```

用途です。

- Mandate Chain。
- Signed Claims。
- Delegation Chain。
- Provenance Chain。

単なる矢印ではなく、`binds`、`authorizes`、`references`などRelationをLabelします。

### D16 / State Transition

Stateがイベントに応じて遷移する図です。

```text
Created → Approved → Executed
             ↓
           Revoked
```

用途です。

- Session Lifecycle。
- Credential Lifecycle。
- Payment State。

### D17 / One-to-Many Delegation

1つのAuthorityやPolicyが複数の実行先へ権限を委任する関係を見せます。

```text
Authority
 ├─▶ Agent A
 ├─▶ Agent B
 └─▶ Agent C
```

用途です。

- Delegation。
- Scope Distribution。
- Fan-out Architecture。

### D18 / Layer Stack

Protocolや責務を上下のLayerとして見せます。

```text
Application
Protocol
Transport
Payment Rail
```

用途です。

- Protocol Stack。
- Responsibility Stack。
- Abstraction Layer。

Architecture Diagramと混同せず、上下関係そのものが論点の時だけ使います。

## Diagram選択ルール

1. まず読者に何を理解させるかを1文で定義します。
2. Relationが重要なら、Relationを表現できるPatternを選びます。
3. 時系列が重要ならSequenceまたはTimelineを選びます。
4. 境界が重要ならArchitecture BoundaryまたはTrust Zoneを選びます。
5. 差分が重要ならBefore / AfterまたはAlternative Comparisonを選びます。
6. Data同士の拘束関係が重要ならData Bindingを選びます。
7. Box + Arrowを描きやすいからという理由だけでPatternを選びません。
8. 1つの図へ複数の主要Relationを詰め込みすぎる場合は図を分割します。

## Diagramの共通配置ルール

- 同格Nodeは同じWidth / Heightを基準にします。
- 同格NodeはCenter Lineを数値で揃えます。
- Box内Textは上下左右中央揃えを基本にします。
- ArrowはNodeのEdgeからEdgeへ接続します。
- ArrowheadをNode内部へ食い込ませません。
- Arrow Labelは線と重ねず、一定のOffsetを取ります。
- NodeとArrow Labelを重ねません。
- Return FlowはPrimary Flowと色または線種を分けます。
- Boundary LineをNodeの文字へ重ねません。
- 図のOuter Paddingを一定にします。

## Compositionとの組み合わせ例

```text
C02 Primary Left + Secondary Right
  + D01 Many-to-One Hub

C04 Full Width Primary
  + D07 Full System Architecture

C05 Equal Split
  + D04 Before / After

C06 Top + Bottom
  + D09 Phase Flow

C04 Full Width Primary
  + D10 Sequence Diagram

C04 Full Width Primary
  + D15 Data Binding Chain
```

CompositionとDiagramを別々に選ぶことで、1つの固定テンプレートへ内容を無理に押し込むことを避けます。
