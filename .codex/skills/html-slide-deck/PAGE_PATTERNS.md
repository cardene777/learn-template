# Page Patterns

このファイルは旧Pattern定義との互換用です。
今後は、ページ構成と図の種類を分離して扱います。

## 参照先

1. `.codex/skills/html-slide-deck/COMPOSITION_PATTERNS.md`
   - スライド全体をどう分割するかを定義します。
   - 固定フレーム、左図＋右説明、全面図、左右比較、上下分割、Column構成などを扱います。
2. `.codex/skills/html-slide-deck/DIAGRAM_PATTERNS.md`
   - 各Region内部へどの種類の図を配置するかを定義します。
   - Hub、Role Separation、Architecture Boundary、Trust Zone、Sequence、Timeline、Data Bindingなどを扱います。

## 原則

スライドを作る時は、次の順序で決めます。

```text
Message
  ↓
Composition Pattern
  ↓
Diagram Pattern
  ↓
Concrete Components
```

`1つの完成テンプレートへ内容を押し込む`方式は使いません。
同じCompositionでもDiagram Patternを差し替えられる構造にします。

例えば次のように組み合わせます。

```text
C02 Primary Left + Secondary Right
  + D01 Many-to-One Hub

C04 Full Width Primary
  + D07 Full System Architecture

C05 Equal Split
  + D04 Before / After

C06 Top + Bottom
  + D09 Phase Flow
```

今後、新しいPatternを追加する場合も、まずCompositionかDiagramかを明確に分類します。
