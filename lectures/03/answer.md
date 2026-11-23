# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
- `--trace` で見えたツール呼び出し（ツール名と引数）：
- 1つの質問での LLM 呼び出し回数（`requests`）：
- 追加したツールと、docstring に書いた説明：

## 宿題

- 取り組んだレベル：基礎
- やったこと：
  - INSTRUCTIONSとget_lecture_summaryのdocstringを以下の2パターン用意し、「uv run python -m app.agent --trace "AIE2026の講座について、第3回では何を学びますか？"」を実行する
    - パターン①（元々の内容）
      ```
      INSTRUCTIONS = """\あなたはAIエンジニアリング講座（AIE2026）の学習支援エージェントです。
      - 用語や講座に固有のことを答える前に、必ず search_glossary で用語集を確認する。
      - 回の内容を聞かれたら get_lecture_summary を使う。
      - 用語集に見つからないことは、推測で断定せず「用語集にはない」と伝える。
      - 回答の最後に、関係する回（第N回）を示す。
      - 宿題の答えそのものは書かず、考え方のヒントで導く。
      """

      def get_lecture_summary(lecture: int) -> str:
          """指定した回（1始まりの整数）の講義の要点を返す。

          「第3回では何を学ぶ？」のように、回の内容や関係を聞かれたときに使う。
          """
      ```
    - パターン②（get_lecture_summaryに関する記述を変更）
        ```
      INSTRUCTIONS = """\あなたはAIエンジニアリング講座（AIE2026）の学習支援エージェントです。
      - 用語や講座に固有のことを答える前に、必ず search_glossary で用語集を確認する。
      
      - 用語集に見つからないことは、推測で断定せず「用語集にはない」と伝える。
      - 回答の最後に、関係する回（第N回）を示す。
      - 宿題の答えそのものは書かず、考え方のヒントで導く。
      """

      def get_lecture_summary(lecture: int) -> str:
          """用語集にない情報が必要になった場合に使う
          """
      ```
- 結果：
  - パターン①
    ```
    [model] gemini-3.5-flash-lite
    第3回では「AIエージェント」について学びます。

    **主な内容：**
    - **AIエージェントの基本構造**: モデル・ループ・ツールを組み合わせた仕組みの理解
    - **ツールとエージェントループ**: LLMがツールを呼び出して次の行動を決める仕組みや、そのコスト（応答時間や料金）の考慮
    - **ハーネスとフレームワーク**: Piや、本線で扱うPydantic AI（型によるツール定義やテスト用モデルなど）、GoogleのADKの活用
    - **ガードレールとHuman-in-the-loop**: 安全性の確保や人の確認を挟む設計

    実際に用語集を検索できるエージェントを作成し、動作確認やツールの追加などの演習も行います。

    （第3回）

    --- trace ---
    [tool call]   get_lecture_summary({'lecture': 3})
    [tool return] get_lecture_summary -> # 第3回 AIエージェント

    ## この回のねらい

    - AIエージェントの基本構造が「モデル＋ループ＋ツール」であることを理解する
    - Pydantic AIで、ツールを使う学習支援エージェントを自分で作り、動かす

    ## 要点

    1.…
    [time] 回答完了まで 4.59 秒（検索・埋め込みを含む）
    [usage] 入力 1,272 tokens / 出力 185 tokens / モデル応答 2 回
    [cost] 生成APIの推定コスト: $0.000844 USD（埋め込み・索引構築分は含まない）
    ```
  - パターン②
    ```
    [model] gemini-3.5-flash-lite
    第3回では、主に「**Pydantic AI**」を用いたPythonでのエージェント開発について学びます。

    具体的には、以下のような内容を扱います。
    * **Pydantic AI**：Pydanticの型システムを使ってツールの引数や出力を定義し、GeminiやOpenAIなどの複数のモデルを統一的な書き方で扱う方法
    * **テスト用モデル**：APIを実際に呼び出さずに動作確認を行う方法
    * **ADK（Agent Development Kit）**（宿題の発展レベル）

    （関係する回：第3回）

    --- trace ---
    [tool call]   search_glossary({'query': '第3回'})
    [tool return] search_glossary -> [{"term": "Pydantic AI", "lecture": 3, "definition": "Pythonでエージェントを作るためのフレームワーク。Pydanticの型を使ってツールの引数や出力を定義でき、GeminiやOpe…
    [time] 回答完了まで 2.42 秒（検索・埋め込みを含む）
    [usage] 入力 1,033 tokens / 出力 144 tokens / モデル応答 2 回
    [cost] 生成APIの推定コスト: $0.000670 USD（埋め込み・索引構築分は含まない）
    ```
- 気づき・疑問：
  - エージェントはINSTRUCTIONSやdocstringを読んで適切にToolを選択していることがわかる。今回の例では、パターン②でget_lecture_summaryについて本来の目的で使う記述を削除、また本来の目的とは異なる記述を行ったところ、「"AIE2026の講座について、第3回では何を学びますか？"」という質問に対してget_lecture_summaryを使わなくなることを確認した。