# Geometry Rules

この文書は、HTML Slide DeckでDiagramを作る時の幾何ルールです。
見た目で線を置かず、Nodeの実座標から接続点を計算します。

## 最優先ルール

DiagramのArrowは固定値で置きません。
Arrowは必ずNodeの接続点から接続点へ引きます。

```text
Node
├── leftCenter
├── rightCenter
├── topCenter
└── bottomCenter
```

## Node定義

Nodeは必ず次の値を持ちます。

```text
x
 y
 width
 height
 centerX = x + width / 2
 centerY = y + height / 2
 leftCenter = [x, centerY]
 rightCenter = [x + width, centerY]
 topCenter = [centerX, y]
 bottomCenter = [centerX, y + height]
```

## Arrow定義

Arrowは次の関数で作ります。

```text
horizontalArrow(from.rightCenter, to.leftCenter)
verticalArrow(from.bottomCenter, to.topCenter)
elbowArrow(from.rightCenter, to.leftCenter, bendX)
```

固定座標で`M360 475 L620 475`のように書いてはいけません。
`from.x + from.width`と`from.y + from.height / 2`から計算します。

## Arrow品質条件

以下を満たさないArrowはFAILです。

1. 始点がNode辺中央に一致している。
2. 終点がNode辺中央に一致している。
3. ArrowheadがNode内部へ食い込んでいない。
4. LabelがArrow上に重なっていない。
5. 直線で済む接続を折れ線にしていない。
6. 水平方向の接続は始点Yと終点Yが一致している。
7. 垂直方向の接続は始点Xと終点Xが一致している。

## Label配置

LabelはArrowの中心点から上下に逃がします。

```text
labelX = (fromX + toX) / 2
labelY = fromY - 18
```

LabelがNodeまたはBoundaryへ近すぎる時は、Arrowを動かさずLabelだけを移動します。

## 可変サイズ

Nodeの文字量が変わる場合でも接続点を再計算します。
Node幅やNode高さを変更した後に、Arrowの座標を手動で残してはいけません。

## 実装条件

SVGを文字列で生成する時も、先にNode配列を定義し、そこからArrowを生成します。

```text
nodesを定義
↓
anchorを計算
↓
arrowsを生成
↓
labelsを生成
↓
nodesを描画
```

描画順はArrowを先、Nodeを後にします。
これにより線がNodeやLabelの上へ出ません。

## 検査

新規Templateを出す前に、少なくとも次を目視または数値で確認します。

1. Node同士の中心線が揃っている。
2. ArrowがNode辺中央から出ている。
3. ArrowがNode辺中央へ入っている。
4. Labelが線やBoxと重なっていない。
5. Content Regionからはみ出していない。
6. 見出しに読点`、`がない。
