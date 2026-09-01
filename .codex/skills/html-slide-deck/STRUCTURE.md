# HTML Slide Deck Directory Structure

このファイルを、テンプレート資産のディレクトリ構造と命名規則の正とします。

## 基本モデル

通常スライドは次の4カテゴリを組み合わせて作ります。

```text
Page
  ↓
Composition
  ├── Diagram
  └── Explanation
```

- `pages/` — ページそのものの種類・外枠。表紙、目次、章扉、通常スライドを含む。
- `compositions/` — 通常スライドのContent Regionをどう分割するかを定義する。
- `diagrams/` — Composition内の図領域へ配置する図そのものを定義する。
- `explanations/` — Composition内の説明領域へ配置する説明表現を定義する。

## パターン単位の必須ファイル

各パターンは1ディレクトリとして管理し、原則として次の3ファイルをセットで持ちます。

```text
{pattern-name}/
├── template.html  # プレースホルダーだけを持つ再利用テンプレート
├── example.html   # 実データを入れた完成サンプル
└── README.md      # 用途、選択条件、制約、プレースホルダーを説明
```

番号は付けません。順番ではなく意味で選ぶため、`left-visual-right-notes`のように用途が分かる名前を使います。

## ディレクトリ構造

```text
pages/
├── cover/
│   ├── centered-title/
│   └── left-title/
├── toc/
│   ├── vertical-list/
│   └── section-grid/
├── section-divider/
│   └── title-only/
└── slide/
    └── header-title-lead/

compositions/
├── left-visual-right-notes/
├── full-visual/
└── split-comparison/

diagrams/
├── architecture/
│   ├── full-boundary/
│   └── layered/
├── flow/
│   └── horizontal-phase/
└── sequence/
    └── standard/

explanations/
├── key-points/
│   └── stacked/
├── numbered-points/
│   └── vertical/
└── comparison/
    └── before-after/
```

## Pageカテゴリ

- `pages/cover/` — 表紙。
- `pages/toc/` — 目次。
- `pages/section-divider/` — 章扉。
- `pages/slide/` — 通常スライドの大枠。

`pages/slide/header-title-lead/template.html`は、現在確定している通常スライド共通フレームです。左上に`{章番号} ／ {セクション名}`、右上に`{ページ番号} / {総ページ数}`、その下に`{タイトル}`とタイトル下部へ重なる強調帯、リード文、Content Regionを持ちます。資料名とFooterは持ちません。

## 既存の旧ファイル

ルート直下の`templates/`、`examples/`、`patterns/`、`references/`にある既存資産は、移行が終わるまでは削除しません。新規テンプレートはこのファイルで定義した4カテゴリ配下へ追加します。
