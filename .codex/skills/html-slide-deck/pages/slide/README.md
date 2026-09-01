# Slide

通常スライドの大枠パターンを管理します。
ここではContent Regionの中身ではなく、ヘッダー、タイトル、リード文、Content Regionの位置までを定義します。

## パターン一覧

- `header-title-lead/`
  - 左上に`{章番号} ／ {セクション名}`、右上にページ数を置く標準外枠です。
  - タイトル下部へ金系の強調帯を重ねます。
  - タイトル下にリード文を置きます。
  - Footerと資料名は持ちません。
  - Content Region内部だけをCompositionへ委譲します。

## 選択ルール

通常の説明ページ、図解ページ、比較ページでは、特別な理由がない限り`header-title-lead/`を使用します。
表紙、目次、章扉は`pages/cover/`、`pages/toc/`、`pages/section-divider/`から選びます。

## パターン追加ルール

通常スライドの外枠を追加する時は、次の3ファイルを必ずセットで作ります。

```text
{pattern-name}/
├── template.html
├── example.html
└── README.md
```

`template.html`はプレースホルダー版、`example.html`は具体的な文字を入れた完成見本、`README.md`は固定座標と変更可能範囲の定義です。
