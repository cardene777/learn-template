# HTML Slide Deck Design System

この文書は、PDFへ出力する前のスライド本体を設計するためのデザイン規則です。
`OWS_REFERENCE_STYLE.md`と承認済みPage Templateを一次基準とし、この文書はそれを補助します。

## 優先順位

視覚判断の優先順位です。

```text
承認済みPage / Composition / Diagram / Explanationの実HTML
↓
OWS_REFERENCE_STYLE.md
↓
QUALITY_GATE.md
↓
このDESIGN_SYSTEM.md
```

一般的なプレゼンテーション設計よりもOWS参照PDFの視覚文法を優先します。

## 基準

- 論理キャンバスは16:9です。
- 1枚の主役は1つだけです。
- 図、比較、フロー、境界、仕様一覧のどれを主役にするかを先に決めます。
- 文字を小さくして収めることを禁止します。
- 収まらない場合はページを分割します。
- 新しい見た目を発明する前に参照PDF内の近いページを探します。

## Page Frame

Pageの外枠は`pages/`配下の承認済みPage Templateを正とします。

通常スライドでは原則として以下を使います。

```text
pages/slide/header-title-lead/
```

CompositionやDiagramがPage Frameを変更してはいけません。
Footerの有無もPage Template側で決めます。

## Typography

1600×900相当のスライドを基準にします。

| 用途 | サイズ |
|---|---|
| Header / meta | 15〜18px |
| Main title | 52〜74px |
| Lead text | 22〜28px |
| Primary diagram label | 20〜32px |
| Secondary diagram label | 15〜20px |
| Annotation | 13〜16px |

本文を18px未満にして情報を押し込んではいけません。

OWS参照PDFでは小さな英字ラベルや番号を補助的に使います。
それらは本文とは別のメタ情報として扱います。

## Alignment

中央揃えをデフォルトにしません。

- Editorial Gridの見出しと説明は左揃えです。
- Structured Listは左揃えです。
- Architecture Nodeの短い名称は中央揃えにできます。
- 長い説明をNode内部へ入れる場合は左揃えを優先します。
- 同格要素は上端、下端、中心線のいずれかを数値で揃えます。
- 視覚重心を中央に置くこと自体を目的にしません。

## Box Usage

Boxは意味がある時だけ使います。

- システム境界。
- Before / Afterの大領域。
- API仕様の補足Box。
- ActorやModuleの実体。
- セキュリティ境界。

以下は禁止します。

- 文章を置くためだけのカード。
- すべての要素を同じBoxで囲むこと。
- 上端に太い色帯を付けたカードUI。
- 丸角と影を使ったWeb UI風の表現。

## Lines

- 枠線は細くします。
- 区切り線は枠線よりさらに軽くします。
- 水平線と垂直線を優先します。
- 折れ線は1回までを基本にします。
- 斜め線は参照PDFに同種表現がある場合だけ使います。
- 矢印がなくても配置で関係を示せる場合は線を増やしません。

## Semantic Color

| 色 | 意味 |
|---|---|
| Green | trusted、verified、accepted、protected |
| Gold | proposed、new、gateway、highlight |
| Red | untrusted、risk、rejected、external |
| Gray | context、existing、boundary |
| Black | primary labels、main structure |

色は装飾ではなく意味を持たせます。
塗りつぶしよりも枠線、ラベル、ハッチを優先します。

## Hatch

斜線ハッチはOWS参照PDFの重要な語彙ですが機械的に使いません。

使ってよい例です。

- NEW要素。
- 提案部分。
- 大きなシステム境界。
- 比較で追加点を見せる領域。

使わない例です。

- すべてのNode。
- すべてのComposition Region。
- 単なる説明Box。

## Reference Archetypes

新しい構図は以下の順に当てはめます。

```text
同格要素             Editorial Grid
仕様一覧             Structured List + Notes
変更前後             Before / After Architecture
時間順               Sequence / Time Flow
境界と内部構造       Boundary / Architecture
```

これらに当てはまらない時は、OWS参照PDF内で視覚的に近いページを探して派生させます。
一般的なHub、Network、Mind Mapへ自動的に逃げません。

## Page Variety

同じ構図を3ページ連続で使ってはいけません。
ただし見た目を変えるためだけに新しい図法を発明しません。
参照PDFに存在する複数のEditorial Patternから選びます。

## OWS Referenceから残す特徴

- 淡いベージュの紙面。
- 細い水平罫線。
- 大きく強い見出し。
- 小さなモノスペース系ラベル。
- 枠線中心の薄いBox。
- Gold、Red、Greenの限定的なSemantic Color。
- 斜線ハッチによる新規領域や境界の強調。
- 左揃えの説明文。
- 余白を使った視線誘導。
- 主役Visualを大きく置きながらも、無理に画面を埋めない構成。

## 完成条件

見た目の完成条件は`QUALITY_GATE.md`のReference Gateを通過することです。
新規Templateは、OWS参照PDFの別ページとして混ぜても違和感が少ない状態にします。
