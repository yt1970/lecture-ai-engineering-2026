# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：glossary_search_glossary
- STEP 2 の [tool call]：glossary_search_glossary({'query': '3レベル'})
- STEP 3 の [tool call]：fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
- STEP 4 の [tool call]：aws_aws___search_documentation({'topics': ['general'], 'search_phrase': 'Amazon S3 バージョニング 概要'})
- 気づき・疑問：エージェントに渡す質問にはどのtoolやMCPを呼ぶように指定していないにも関わらず、きちんとモデルがMCPを特定してMCPを呼び出している部分が不思議に思えました。MCP_agent.pyを見てみると、MCP_config.jsonからリストを作ってモデルに渡している処理やプロンプトは確認できたが、それだけで確実にMCPを呼び出すためには能力の高いモデルを使うことやモデルの学習が必要なのではないかと感じました。

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：基礎 及び実装
-  やったこと：get_lecture_summaryとmake_quizの２つのツールをMCP_surver.pyで公開しました。
- 結果：モデルから呼び出してツールを使うことができました。ただし、make_quize については、問題を出題した後、回答を受け付けて正解か否かを回答する複数ターンの会話をagent.pyで実装していたが、MCP_agent.pyではその部分を実装していなかったので出題だけで終わってしまった。
- 気づき・疑問：MCPは他の方が作ったツールを容易に利用できるという利点があるが、agent.pyなどでモデルの挙動をコーディングしてしまった場合、MCPのツールが想定していた範囲ではうまく動かない可能性があることがわかりました。MCP上のツールがどのようなリターンを返すのかを想定して、エージェント（MCPの枠組みで言えば、MCPクライアント）の部分の実装を変える必要があると感じました。
