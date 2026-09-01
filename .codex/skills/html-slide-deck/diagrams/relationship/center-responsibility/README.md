# Center Responsibility

中心要素と周辺要素の関係を示すDiagram Templateです。

## 用途

- 1つの中心要素が要求を受ける時に使います。
- 中心要素が評価先と委譲先へ処理を分ける時に使います。
- OWS参照PDFのBoundaryとArchitectureの視覚文法に合わせます。

## 構成

```text
OUTSIDE        CORE PROCESS        CONTROL
要求元   →     中心要素      →     評価と委譲
```

## 配置

- Content Regionは`x=80, y=315, w=1440, h=505`です。
- 左は要求元Zoneです。
- 中央は中心要素Zoneです。
- 右は評価と委譲Zoneです。
- ArrowはNodeの辺中央から辺中央へ接続します。
- Arrow座標はNode定義から計算します。

## 可変対応

- Nodeの`x y w h`から接続点を計算します。
- Arrowは固定座標で直接指定しません。
- LabelはArrowの中点から上方向へ逃がします。
- Nodeの幅や高さを変えてもArrowがずれない構造にします。

## 禁止

- 斜めArrowは使いません。
- Node上端に太い色帯を付けません。
- 丸角と影を使いません。
- 見出しに読点を入れません。
