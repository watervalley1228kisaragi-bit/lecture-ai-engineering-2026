# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前： glossary_search_glossary
- STEP 2 の [tool call]： glossary_search_glossary({'query': '3レベル'})
- STEP 3 の [tool call]： fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
- STEP 4 の [tool call]：
  - aws_aws___search_documentation({'search_phrase': 'Amazon S3 バージョニング 概要'})
  - aws_aws___search_documentation({'search_phrase': 'What is S3 Versioning', 'topics': ['general']})
- 気づき・疑問：
  - 複数MCPサーバーのツールにプレフィックス（glossary_、fetch_、aws_）が付与され、用途に応じて使い分けられている。
  - STEP 4では日本語と英語のクエリを並列で呼び出し、情報取得の網羅性を高めている。
  - サーバー名とツール名の重複による命名の冗長化が、ツール選択の精度やトークン消費にどの程度影響するか疑問である。

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：基礎 / 実装 / 発展
- やったこと：
- 結果：
- 気づき・疑問：
