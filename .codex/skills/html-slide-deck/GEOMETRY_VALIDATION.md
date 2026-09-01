# Geometry Validation

新規TemplateとExampleを作成する時は、見た目の確認だけでなく座標検査を行います。

## 必須検査

1. Content Regionの範囲を固定します。
   - 通常スライドでは`x=80, y=315, w=1440, h=505`を基準にします。
2. 全NodeがContent Region内に収まることを確認します。
   - Nodeの`x, y, width, height`を数値で検査します。
3. 全Textが所属Node内に収まることを確認します。
   - Textの想定幅がNode幅から左右余白を引いた値を超えないことを確認します。
4. Arrowの始点と終点をNode辺中央に接続します。
   - 左から右へ進むArrowは`from.rightCenter`から`to.leftCenter`へ接続します。
   - 上から下へ進むArrowは`from.bottomCenter`から`to.topCenter`へ接続します。
5. ArrowheadがNode内へ食い込まないようにします。
   - 終点はNode辺の手前で止めず、markerのrefXを考慮してNode辺中央に合わせます。
6. LabelがArrowやNodeへ重ならないことを確認します。
   - LabelはArrowの中点から上下に18px以上離します。
7. 見出しに読点を含めないことを確認します。
   - `、`を含む見出しはFAILです。

## 生成時の実装ルール

Nodeは辞書または配列で定義し、ArrowはNode定義から接続点を計算します。
Arrow座標を手入力してはいけません。

```text
Node
  x
  y
  w
  h
  leftCenter
  rightCenter
  topCenter
  bottomCenter

Arrow
  fromNode
  fromAnchor
  toNode
  toAnchor
  label
```

## FAIL時の扱い

1つでもFAILがある場合はTemplateとして追加しません。
まずHTMLを修正し、検査結果をPASSにしてからユーザーへ提示します。
