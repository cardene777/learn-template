# Markdown and Mermaid Rules

このファイルはノートでMarkdownとMermaidを使う時の共通ルールです。

## 基本方針

Markdownの記述方法を十分に活用します。

文章だけを延々と続けるのではなく、情報の種類に合う表現を選びます。

ただし、装飾のためだけにTableや図を増やしません。

## 見出しは意味が通る日本語で書く

ユーザー向けノートの`title`、`##`、`###`、`####`は、ユーザーが別言語を明示しない限り日本語を既定とします。

英語の公式見出しを単語単位で直訳しただけの見出しや、英語の概念名へ`の仕組み`を付けただけの見出しを作ってはいけません。

見出しだけを読んでも「このSectionで何が分かるか」が日本語で伝わる表現にします。

固有名詞、Protocol名、API名、Schema名、Field名、RFC名など原文維持が必要な識別子は残して構いません。ただし、その周囲の説明語は自然な日本語へ置き換えます。

良い例:

```text
AP2 v0.2で誰が何を担当するか
利用者の権限をAgentへ委任して検証する仕組み
Merchantが確定したCheckoutへ権限を固定する
支払い権限と実際の決済Credentialを分ける
A2Aは通信、AP2は権限証明を担当する
AP2互換のx402連携はまだ完成していない
```

避ける例:

```text
5 Roles
Agent Authorization Frameworkの仕組み
Checkout MandateとCheckout Receipt
Payment MandateとPayment Receipt
Current Source
Runtime Architecture
Security and Privacy
Implementation Considerations
```

公式文書のTitleを残したい場合は、本文中のSource名やMetadataで保持し、ユーザー向け見出しは内容責務を日本語で表します。

保存前に全見出しを走査し、次を確認します。

- 英語だけの一般概念見出しが残っていない。
- 英語語句を日本語助詞でつないだだけの見出しになっていない。
- `〜の仕組み`だけで意味を曖昧にしていない。
- 見出しと直下本文の中心質問が一致している。
- 固有名詞を翻訳しすぎて検索性を落としていない。

`Literal Translation Heading = 0`、`Meaningless English Heading = 0`を完成条件とします。

## Markdownを直接使う

通常の説明はMarkdown本文へ直接書きます。

- Paragraphは理由、因果関係、仕組みの説明に使う。
- `inline code`はAPI、Field、Header、Identifier、Command、Config値などに使う。
- **Bold**は重要な結論を限定的に強調する。
- Unordered Listは順序のない条件、特徴、構成要素に使う。
- Ordered Listは順序に意味がある手順に使う。
- Tableは比較、Role差分、Field対応、条件と結果の対応に使う。
- Blockquoteは重要なInvariant、注意点、境界を短く強調する時に使う。
- Footnoteは本文の主線から外れる補足に使う。
- `<details>` / `<summary>`は補助的な長いPayload、旧Version差分、追加例、用語補足に使える。
- Markdown Linkは一次資料や仕様への参照に使う。

重要な前提、主要Flow、Security RequirementをFootnoteや`details`へ隠しません。

## 用語補足トグル

初学者が本文を読む時に外部検索しないと意味を確定できない用語は、初出付近に補足トグルを置きます。
概要ノートと仕組みノートでは、この規則を必須とします。

### トグル対象

次のどれかに当てはまり、本文理解へ影響する語は原則トグル対象です。

- 略語や頭字語。例: `SD-JWT`、`TEE`、`JCS`。
- Protocol、Standard、Extension、Profile名で、名前だけでは役割が分からないもの。
- 仕様固有のRole、Object、Evidence、Mandate、Receipt、Credentialなど、日常語と意味がずれるもの。
- 暗号、認証、認可、署名、Hash、Binding、Delegationなど、誤解すると保証範囲を取り違える用語。
- Schema / Claim / Field名で、後続Flowを理解するため意味の補足が必要なもの。
- Draft、Candidate、Final、ExperimentalなどVersion / Standardization Statusを誤解しやすいもの。
- 類似概念との区別が必要なもの。

一般的なHTTP、JSON、URLのように対象読者が通常理解しており、本文の意味も変わらない語へ機械的にトグルを付けません。
ただし、その記事では一般的な意味と違う使い方をする場合は対象にします。

### 本文とトグルの責任分担

重要Conceptの本質をトグルへ隠してはいけません。
本文には最低限、その語が**この文脈で何をするものか**を短く書きます。

トグルには、本文の主線を止めずに読める補足として、必要に応じて次を入れます。

- 正式名称や略語の展開。
- 平易な定義。
- この技術でなぜ登場するか。
- 何と混同しやすいか。
- 何を保証し、何を保証しないか。
- 短い具体例。
- 関連Standardや仕様上の位置付け。

主要Flow、MUST / SHOULD / MAY、Security Requirement、Version上の重要差分、実装判断に必須の情報は本文にも残します。

### トグルは1行辞書で終わらせない

`Needs Toggle = Yes`の語について、**略語の展開と1文定義だけを書いてCovered扱いにしてはいけません。**
特にProtocol、Standard、Schema、Credential、Evidence、Message、Role、Security Mechanism、仕様固有Objectは、読者がそのトグルだけを開いて「具体的に何なのか」を理解できる深さまで補足します。

必要に応じて次を説明します。

1. 平易な日本語で何を表すものか。
2. この記事のどの場面で必要になるか。
3. 実際にどんな形をしているか。
4. 誰が作成・保持・送信・検証・利用するか。
5. 主要な構成要素やFieldが何を表すか。
6. Flow上で次の何へ使われるか。
7. 似た概念とどう違うか。
8. Versionや標準化Statusに注意が必要なら現在の位置付け。
9. 短い具体例。

Data Object、Schema、Credential、Message、Tokenのように**形式そのものが理解に重要な用語**では、一次情報で確認できる範囲で代表的な形を示します。
例えば、Field一覧、短いJSON断片、Request / Response断片、構造Tableなどを使います。
公式に固定された形式が無い、まだDraftで形が変わり得る、Conceptだけ定義されている場合は、形式を捏造せず、その状態を説明します。

RoleやComponentなら、名前の意味だけではなく、主なInput、Output、責任、後続の利用先を説明します。
Mechanismなら、定義だけではなく、何を入力にして何を確認し、結果が何に使われるかを短いFlowとして説明します。

トグル内で新しい専門用語を増やした場合、その語も読者が理解できる日本語でその場で説明するか、不要なら使わないようにします。
**未知語を未知語で説明してトグルを閉じてはいけません。**

`最初に押さえる基本用語`へ複雑な用語を大量に1行ずつ並べるだけでは不十分です。
重要な語は、本文の初出付近に`<用語>を具体的に見る`、`<用語>の中身`、`<用語>がFlowでどう使われるか`のような独立したトグルを置いて構いません。
トグルは用語辞典ではなく、**本文の流れを壊さず理解を深める補助Section**として使います。

### 正式なMarkdown記法

Source Markdownには装飾用Classや`markdown="1"`を書きません。
トグルはHTML標準の`<details>` / `<summary>`だけで、次のようにシンプルに記述します。

~~~html
<details>
<summary>NonceとReplayを具体的に見る</summary>

`Nonce`は、同じRequestを後からそのまま使い回しにくくするため、1回の処理へ割り当てる値です。
Requestへ含め、受信側が「自分が発行した値か」「まだ使われていないか」を確認します。

例えばPayloadの一部は次のような形になります。

```json
{
  "nonce": "7f3c..."
}
```

1. ServerがNonceを発行します。
2. ClientはそのNonceをRequestや署名対象へ含めます。
3. Serverは受信時にNonceが期待した値か、未使用かを確認します。
4. 受理したNonceを使用済みにします。

過去のValidなRequestをそのまま再送する`Replay`を検知しやすくするために使います。

</details>
~~~

このRepositoryではKramdownの`parse_block_html`を有効にし、`details`内部のMarkdownをBuild時に自動Renderします。
色、枠、余白、開閉Iconなどの見た目は`assets/article-overrides.css`が`.content details`へ自動適用します。
**NoteのMarkdownへPresentation用ClassやStyleを書いてはいけません。**

用語ごとに別トグルへ分ける必要はありません。
近い文脈で最初に必要になる単純な用語は、`最初に押さえる基本用語`のような1つのトグルへまとめて構いません。
一方で、Data ShapeやFlowまで理解しないと意味が閉じない複雑な用語を、短い一行だけに圧縮して同じトグルへ押し込みません。
長くなりすぎる場合は、`署名と検証の用語`、`取引状態の用語`のように意味単位で分けるか、重要語を独立トグルへ分けます。

`summary`は読者が開く目的をすぐ判断できる短い日本語にします。

- `最初に押さえる基本用語`
- `署名と検証の用語`
- `この仕様で使うRole`
- `<用語>を具体的に見る`
- `<用語>の中身`
- `<用語A>と<用語B>の違い`

トグルを連続して大量に並べて用語辞典化しません。
本文の初出箇所に近い位置へ置き、読者が必要な時だけ開けるようにします。

### 用語トグル完成条件

概要ノートと仕組みノートでは、保存前にTerm / Concept Ledgerと本文を照合します。

- `Needs Toggle = Yes`なのに対応する`<details>`がない用語は0件。
- `Needs Toggle = Yes`なのに略語展開＋1文定義だけで終わる重要語は0件。
- Data Shapeが理解に必要なのに、具体的な形式や構成要素の説明が無い重要語は0件。
- トグル内の説明を理解するため外部検索が必要な未知語は0件。
- トグルだけに中心説明を隠している重要Conceptは0件。
- 同じ用語の重複トグルは原則0件。
- `summary`だけでは何の補足か分からないトグルは0件。
- MarkdownがRenderされず生の`<details>`文字列が見える箇所は0件。

`Shallow Required Toggle = 0`、`Complex Data Toggle Without Shape = 0`、`Toggle External Lookup Dependency = 0`を完成条件とします。

## Code Block

Code Blockは固定幅表現が必要なものだけに使います。

対象は主に以下です。

- Code。
- Command。
- Config。
- Request / Response Payload。
- Schema。
- Log。
- 生Data。
- Mermaid Source。

通常の説明、条件集合、比較、概念関係、処理順を`text` Code Blockへ入れません。

次のようなASCII擬似図は禁止します。

```text
A
+
B
↓
Decision
```

FlowならMermaid、比較ならTable、条件ならListを使います。

## Markdown上の図

このRepositoryでMarkdownへ直接記述するDiagram DSLはMermaidだけを使います。

PlantUML、Graphviz、D2など追加Rendererが必要な記法は使いません。

## Mermaid公式ドキュメントを必ず確認する

Mermaidを書く前に、記憶だけでSyntaxを書いてはいけません。

必ず公式ドキュメントを確認します。

最初に次を開きます。

- `https://mermaid.js.org/intro/`

その上で、実際に使用するDiagram Typeの公式Syntaxページを開いて記法を確認します。

例えば`sequenceDiagram`を使うならSequence Diagram、`stateDiagram-v2`を使うならState Diagramの公式Syntaxを確認します。

1つのノートで複数のDiagram Typeを使う場合は、使用するTypeごとに公式Syntaxを確認します。

公式Introに掲載されているDiagram Typeの中から目的に合うものを選びます。Flowchartへ何でも押し込みません。

候補には例えば以下があります。

- Flowchart。
- Swimlanes Diagram。
- Sequence Diagram。
- Class Diagram。
- State Diagram。
- Entity Relationship Diagram。
- User Journey。
- Gantt。
- Requirement Diagram。
- GitGraph。
- C4 Diagram。
- Mindmap。
- Timeline。
- Sankey。
- Block Diagram。
- Packet Diagram。
- Architecture Diagram。

実際に利用可能か、現在のSyntaxが何かは公式ドキュメントをその都度確認します。

## Diagram Typeの選択

図の種類は「何を見せたいか」で決めます。

| 見せたいもの | 主な候補 |
|---|---|
| 時間順の通信 | Sequence Diagram |
| 条件分岐・処理順 | Flowchart |
| 状態遷移 | State Diagram |
| EntityやDataの関係 | ER / Class Diagram |
| Component配置やArchitecture | Architecture / Block / C4 / Flowchart |
| Conceptの階層 | Mindmap |
| 時系列 | Timeline / Gantt |
| Requirementの関係 | Requirement Diagram |
| User体験の流れ | User Journey |

公式により適したDiagram Typeがあるなら、慣れているという理由だけでFlowchartを選びません。

## Mermaidの内容

図は本文の代用品ではありません。

図の前後で、何を見る図なのか、どう読めばよいのかを本文で説明します。

図だけに重要な概念を追加しません。

本文と図で同じ概念には同じ名前を使います。

Labelは短くし、長い説明文をNodeへ詰め込みません。

Sequence Diagramの`participant`には実際にMessageを送受信する主体を置きます。処理名や判定名をParticipantにしません。

Architecture図ではComponent、Boundary、Connectionの意味を明確にします。

State DiagramではStateとTransition Conditionを混同しません。

## Mermaidを使うべきでない場合

次の場合はMermaidを使いません。

- 4つの条件を並べるだけならListで十分な場合。
- 2つの概念を比較するだけならTableの方が速く読める場合。
- 図が本文と全く同じ内容を重複するだけの場合。
- Nodeが大量になり、図を見る方が理解しにくくなる場合。

## Render確認

保存前にMermaid Syntaxが公式記法に沿っていることを確認します。

可能な場合はRepositoryのBuildを実行し、MarkdownとMermaidを含むページが正常にRenderできることを確認します。
