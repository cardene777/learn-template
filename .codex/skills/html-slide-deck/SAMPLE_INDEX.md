# HTML Slide Deck Sample Index

現在リポジトリにあるスライド、Composition、Diagram、Explanationのテンプレートとサンプル一覧です。

凡例：

- ✅ 実装済み。現在のデザイン基準として利用可能です。
- 🚧 プレースホルダー。ディレクトリ構造だけあり、HTMLは未実装またはTODOです。
- 🧪 Legacy / Reference。移行前の検証・参照用です。

## Pages

| Status | Pattern | Template | Example |
|---|---|---|---|
| ✅ | Cover / Left Title | [template](pages/cover/left-title/template.html) | [example](pages/cover/left-title/example.html) |
| 🚧 | Cover / Centered Title | [template](pages/cover/centered-title/template.html) | [example](pages/cover/centered-title/example.html) |
| ✅ | TOC / Section Grid | [template](pages/toc/section-grid/template.html) | [example](pages/toc/section-grid/example.html) |
| 🚧 | TOC / Vertical List | [template](pages/toc/vertical-list/template.html) | [example](pages/toc/vertical-list/example.html) |
| ✅ | Section Divider / Title Only | [template](pages/section-divider/title-only/template.html) | [example](pages/section-divider/title-only/example.html) |
| ✅ | Slide / Header Title Lead | [template](pages/slide/header-title-lead/template.html) | [example](pages/slide/header-title-lead/example.html) |

## Compositions

CompositionはContent Regionの大きな分割だけを定義し、DiagramやExplanationの内部構造は持ちません。

| Status | Pattern | Template | Example |
|---|---|---|---|
| ✅ | Left Visual / Right Notes | [template](compositions/left-visual-right-notes/template.html) | [example](compositions/left-visual-right-notes/example.html) |
| ✅ | Full Visual | [template](compositions/full-visual/template.html) | [example](compositions/full-visual/example.html) |
| ✅ | Split Comparison | [template](compositions/split-comparison/template.html) | [example](compositions/split-comparison/example.html) |
| ✅ | Two Phase | [template](compositions/two-phase/template.html) | [example](compositions/two-phase/example.html) |
| ✅ | Four Elements | [template](compositions/four-elements/template.html) | [example](compositions/four-elements/example.html) |

## Diagrams

| Status | Pattern | Template | Example |
|---|---|---|---|
| ✅ | Sequence / Standard | [template](diagrams/sequence/standard/template.html) | [example](diagrams/sequence/standard/example.html) |
| 🚧 | Architecture / Full Boundary | [template](diagrams/architecture/full-boundary/template.html) | [example](diagrams/architecture/full-boundary/example.html) |
| 🚧 | Architecture / Layered | [template](diagrams/architecture/layered/template.html) | [example](diagrams/architecture/layered/example.html) |
| 🚧 | Flow / Horizontal Phase | [template](diagrams/flow/horizontal-phase/template.html) | [example](diagrams/flow/horizontal-phase/example.html) |

## Explanations

現時点ではExplanationカテゴリは構造のみで、実HTMLはプレースホルダーです。

| Status | Pattern | Template | Example |
|---|---|---|---|
| 🚧 | Key Points / Stacked | [template](explanations/key-points/stacked/template.html) | [example](explanations/key-points/stacked/example.html) |
| 🚧 | Numbered Points / Vertical | [template](explanations/numbered-points/vertical/template.html) | [example](explanations/numbered-points/vertical/example.html) |
| 🚧 | Comparison / Before After | [template](explanations/comparison/before-after/template.html) | [example](explanations/comparison/before-after/example.html) |

## Legacy / Reference Samples

| Status | Sample | Purpose |
|---|---|---|
| 🧪 | [A01 Full Architecture](examples/a01-full-architecture-sample.html) | OWSスタイルのフルアーキテクチャ検証用 |
| 🧪 | [PDF Viewer Sample](examples/pdf-viewer-sample.html) | PDFビューア形式の検証用 |

## Current usable set

現在、実装済みとして扱うパターンは以下です。

1. Cover / Left Title
2. TOC / Section Grid
3. Section Divider / Title Only
4. Slide / Header Title Lead
5. Left Visual / Right Notes
6. Full Visual
7. Split Comparison
8. Two Phase
9. Four Elements
10. Sequence / Standard

プレースホルダーは、実装・レビューが終わるまで生成時の標準候補として扱わないでください。
