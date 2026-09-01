---
name: html-slide-deck
description: OWS参照資料から抽出したPage、Composition、Diagram、Explanationの実HTMLテンプレートとサンプルを組み合わせて高品質PDFを作成し、そのPDFをサムネイルサイドバー付きHTMLビューアへ変換する。
---

# HTML Slide Deck

このSkillは、技術解説や提案資料を高品質なPDFスライドとして作成し、そのPDFをPDFビューア風HTMLへ変換するためのSkillです。
HTMLは閲覧器であり、スライド本文のデザイン品質はPDF作成段階で決めます。

## 最優先ルール

**Markdownの説明だけを読んでスライドを生成してはいけません。**
実際にレンダリング確認済みの`template.html`と`example.html`を必ず開き、その座標、余白、線、背景、領域サイズを基準に実装します。

視覚実装の優先順位です。

```text
各パターンのtemplate.html / example.html
↓
各パターンのREADME.md
↓
GEOMETRY_RULES.md
↓
OWS_REFERENCE_STYLE.md / DESIGN_SYSTEM.md
↓
QUALITY_GATE.md
```

MarkdownとHTMLが食い違う場合は、レンダリング確認済みHTMLを優先します。

## 設計モデル

スライドは1つの完成テンプレートとして扱いません。
次の4カテゴリを合成します。

```text
Page
↓
Composition
├── Diagram
└── Explanation
```

- `pages/`
  - 表紙、目次、章扉、通常スライドなどのページ外枠です。
- `compositions/`
  - 通常スライドのContent Regionをどう分割するかを定義します。
- `diagrams/`
  - Composition内の図領域へ配置する図そのものを定義します。
- `explanations/`
  - Composition内の説明領域へ配置する説明表現を定義します。

各パターンは原則として次の3ファイルをセットで持ちます。

```text
{pattern-name}/
├── template.html
├── example.html
└── README.md
```

番号は付けません。
順番ではなく意味で選ぶため、用途が分かるパターン名を使います。

## 実装前に必ず確認するファイル

1. `.codex/skills/html-slide-deck/STRUCTURE.md`
   - 4カテゴリ、ディレクトリ構造、命名規則の正です。
2. 使用するPageパターンの`template.html`、`example.html`、`README.md`
3. 使用するCompositionパターンの`template.html`、`example.html`、`README.md`
4. 図がある場合は使用するDiagramパターンの`template.html`、`example.html`、`README.md`
5. 説明領域がある場合は使用するExplanationパターンの`template.html`、`example.html`、`README.md`
6. `.codex/skills/html-slide-deck/GEOMETRY_RULES.md`
7. `.codex/skills/html-slide-deck/OWS_REFERENCE_STYLE.md`
8. `.codex/skills/html-slide-deck/DESIGN_SYSTEM.md`
9. `.codex/skills/html-slide-deck/QUALITY_GATE.md`
10. `.codex/skills/html-slide-deck/templates/pdf-viewer-slide-deck.html`
11. `.codex/skills/html-slide-deck/tools/pdf_to_viewer_html.py`

ルート直下の旧`templates/`、`examples/`、`patterns/`、`references/`は移行中の互換資産です。
新規テンプレートは`STRUCTURE.md`で定義した4カテゴリ配下へ追加します。

## 通常スライドの標準Page

通常スライドでは、原則として次を使用します。

```text
pages/slide/header-title-lead/
├── template.html
├── example.html
└── README.md
```

固定ルールです。

- 左上は`{章番号} ／ {セクション名}`です。
- 右上は`{ページ番号} / {総ページ数}`です。
- `{資料名}`は置きません。
- Footerは置きません。
- タイトルは`x=80`、baseline `y=185`を基準にします。
- タイトル下部へ金系の強調帯を重ねます。
- 強調帯は文字幅にぴったり合わせます。
- リード文は`x=80`、baseline `y=265`を基準にします。
- Content Regionは`x=80, y=315, w=1440, h=505`です。
- Compositionが変更してよいのはContent Region内部だけです。

## Page制作ルール

- 表紙、目次、章扉、通常スライドは別Pageパターンとして扱います。
- Pageパターンごとに`template.html`、`example.html`、`README.md`を持たせます。
- 通常スライドのタイトル位置やヘッダー位置をCompositionごとに動かしてはいけません。
- Content Regionを広げるためにヘッダーやタイトルを削ってはいけません。

## Composition制作ルール

- CompositionはPageのContent Region内部だけを分割します。
- ヘッダー、タイトル、リード文をComposition側で再定義しません。
- RegionのTop、Bottom、Width、Gapは実HTMLで固定します。
- 左右Regionの上端と下端を数値で揃えます。
- 新規Compositionも、先に`template.html`と`example.html`を作ってレンダリング確認してからREADMEへ定義します。

## Diagram制作ルール

図は必ずこの順序で作ります。

1. 参照PDFから近い図を1枚選びます。
2. 対応するDiagramパターンの実HTMLを開きます。
3. 参照図の背景ハッチ、Zone枠、ラベル位置、線幅、色、余白を基準にします。
4. 内容だけをプレースホルダー化します。
5. Node配列を定義します。
6. Nodeの`x`、`y`、`width`、`height`から接続点を計算します。
7. Arrowは接続点から接続点へ生成します。
8. LabelはArrowの中点から一定距離だけ逃がします。
9. 同格NodeのWidth、Height、Center Lineを数値で揃えます。
10. Arrowは水平直線、垂直直線、1回だけ曲がる直交折れ線の順に優先します。
11. 斜めArrowは原則使いません。
12. SVGなど単一の固定座標系で実装します。
13. 画像としてレンダリングし、参照図と並べて確認します。

Diagramパターンは図そのものだけを持ちます。
Pageのヘッダー、タイトル、リード文、FooterなどをDiagram側へ含めてはいけません。

## Geometry必須ルール

Arrowを見た目で置いてはいけません。
Arrowは必ずNodeの辺中央から辺中央へ接続します。

```text
leftCenter   = [x, y + height / 2]
rightCenter  = [x + width, y + height / 2]
topCenter    = [x + width / 2, y]
bottomCenter = [x + width / 2, y + height]
```

水平Arrowは以下で生成します。

```text
start = from.rightCenter
end   = to.leftCenter
```

垂直Arrowは以下で生成します。

```text
start = from.bottomCenter
end   = to.topCenter
```

Arrowを固定座標で直接書くことを禁止します。
固定座標が必要な場合でも、先にNode定義から計算した値を使います。

## Geometry検査

Templateを見せる前に必ず検査します。

1. 水平Arrowの始点Yと終点Yが一致している。
2. 垂直Arrowの始点Xと終点Xが一致している。
3. Arrow始点がNode辺中央に一致している。
4. Arrow終点がNode辺中央に一致している。
5. ArrowheadがNode内部へ食い込んでいない。
6. LabelがArrowやNodeへ重なっていない。
7. 同格Nodeの幅と高さが揃っている。
8. Content Regionから要素がはみ出していない。
9. 見出しに読点`、`が入っていない。

1つでも満たせない場合は出力してはいけません。

## Explanation制作ルール

- Explanationは説明領域の視覚表現だけを定義します。
- 箇条書き、番号付き要点、比較説明、結論などをパターン化します。
- CompositionのRegionサイズを変更してはいけません。
- 説明量が多すぎる時は文字を縮小するのではなく、Page分割または別Compositionへの切り替えを優先します。

## 作成フロー

1. Sourceを調査します。
2. Slide Inventoryを作ります。
3. Pageパターンを選びます。
4. 通常スライドならCompositionパターンを選びます。
5. 必要なDiagramとExplanationパターンを選びます。
6. 各パターンの`template.html`と`example.html`を開きます。
7. OWS Reference Styleを適用します。
8. NodeとRegionを固定座標で定義します。
9. ArrowとLabelをNode接続点から生成します。
10. Geometry検査を通します。
11. PDFを作成します。
12. Montageを作成します。
13. `QUALITY_GATE.md`で判定します。
14. PDFをHTML Viewerへ変換します。
15. PC幅とスマホ幅でViewerを検証します。

## 配置ルール

- Webページのような可変reflowをスライド本体へ使いません。
- 1600×900の固定座標を基準にします。
- DiagramはSVGなど単一座標系で描くことを優先します。
- 同格NodeのWidth、Height、Center Lineを数値で揃えます。
- 左右RegionのTop、Bottomを数値で揃えます。
- Box内Textは上下左右中央揃えを基本にします。
- ArrowはNode EdgeからNode Edgeへ接続します。
- ArrowheadをNodeへ食い込ませません。
- Labelを線やNodeへ重ねません。
- 直線で済むArrowを折れ線にしません。
- 斜めArrowをデフォルトにしません。

## スライド本体の必須条件

- 1ページ1メッセージにします。
- 各ページに主役Visualを置きます。
- 複雑なArchitectureは狭い左右分割へ詰めず、全面図へ切り替えます。
- 本文を18px未満にして押し込みません。
- 同じCompositionを3ページ連続で使いません。
- 同じDiagramパターンを機械的に連続使用しません。
- 図の種類は伝えるRelationに合わせて選びます。
- BoxとArrowが簡単だからという理由で図を決めません。

## Viewer必須条件

- 左サイドバーは常時表示します。
- サイドバーはタイトル一覧ではなく各ページのサムネイル一覧です。
- active枠はサムネイル画像だけに付け、番号は囲みません。
- サムネイルをタップすると対応ページへ移動します。
- 移動後、サイドバー内のactive枠も対応ページへ移動します。
- スマホでもサイドバーを消しません。

## 禁止事項

- Markdown定義だけを読んで実HTMLを見ずに生成すること。
- レンダリング確認済みテンプレートを使わず毎回ゼロから座標を推測すること。
- Page、Composition、Diagram、Explanationを混同すること。
- Diagramテンプレートへタイトルやヘッダーを含めること。
- Compositionごとにタイトル位置やヘッダー位置を変えること。
- 参考PDFを見ずに汎用箱図から作り始めること。
- OWSの背景ハッチや境界表現を理由なく捨てること。
- 小さい箱と矢印だけの簡易図へ逃げること。
- カード横並びをデフォルトにすること。
- 複雑な図を狭いRegionへ押し込むこと。
- 文字を小さくして1ページへ詰め込むこと。
- Arrowを固定座標の目分量で置くこと。
- Montage Reviewなしで完成扱いすること。
- Viewerだけ正常でスライド本体が弱いものを完成扱いすること。

## 完成条件

完成とはHTMLファイルが存在する状態ではありません。
選択したPage、Composition、Diagram、Explanationの実HTMLテンプレートとサンプルを基準にしたPDFが`QUALITY_GATE.md`を通過し、そのPDFがViewerテンプレートへ変換され、PCとスマホの両方で確認できる状態を完成とします。
