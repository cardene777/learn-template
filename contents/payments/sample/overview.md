---
id: sample-payments-overview
permalink: /payments/sample/overview.html
title: 決済のサンプルノート
description: Learn Templateの表示・編集とdetails/code表示を確認するための最小サンプルです。
type: Note
order: 10
domainId: payments
domainName: 決済
collectionId: sample
collectionName: サンプル
placementLocked: false
---

## このノートについて

このページはTemplate repositoryの動作確認用サンプルです。

以下のトグルはdetails、定義行、コード表示のSmoke Testにも使います。

<details>
<summary>サンプルAPIの主要フィールド</summary>

- `requestId`: リクエストを識別するサンプルIDです。
- `status`: 処理状態を表すサンプル値です。

```json
{
  "requestId": "demo-1",
  "status": "ok"
}
```

</details>

## 編集確認

`本文編集`からこのMarkdownを変更して保存すると、自分のGitHub repositoryへCommitが作られ、GitHub Actions経由でCloudflareへ再デプロイされます。
