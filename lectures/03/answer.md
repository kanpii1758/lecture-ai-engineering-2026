# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：素のLLMはAIE2026を一般的な講座だと推測し、基礎・標準・応用という一般論を回答した。エージェントは用語集を検索し、「基礎（講義内容の確認）・実装（自分でコードを書く）・発展（調査や試行）」の3段階からどれか1つを選べば完了、と講座固有の内容を正しく回答した。
- `--trace` で見えたツール呼び出し（ツール名と引数）：`search_glossary({'query': 'LoRA'})`、`search_glossary({'query': 'QLoRA'})`。追加ツールの確認では `make_quiz({'lecture': 2})` が呼ばれた。
- 1つの質問での LLM 呼び出し回数（`requests`）：LoRAとQLoRAの比較は2回（`tool_calls=2`）。第2回の確認問題は2回（`tool_calls=1`）。
- 追加したツールと、docstring に書いた説明：`make_quiz(lecture: int) -> str` を追加した。指定した講義回の用語から復習問題を1問作り、問題と答えを返すツールで、「第2回の確認問題を出して」のように指定回の復習問題を求められたときに使う、と説明した。用語がない回では例外にせずメッセージを返す。
- 動作確認：`--list-tools` で3ツール（`search_glossary`、`get_lecture_summary`、`make_quiz`）を確認。`uv run pytest -q` は `15 passed`。実行時には第2回の「エポック」の確認問題が出題された。

## 宿題

- 取り組んだレベル：基礎
- やったこと：`app/agent.py` の `INSTRUCTIONS` から「用語や講座に固有のことを答える前に、必ず search_glossary で用語集を確認する。」という1行だけを削除した。ほかの設定と質問文は変えず、変更前後で同じ `uv run python -m app.agent --trace "LoRAとQLoRAの違いは？"` を実行した。
- 結果：変更前は `search_glossary({'query': 'LoRA'})` と `search_glossary({'query': 'QLoRA'})` が呼ばれ、`requests=2`、`tool_calls=2`。変更後も同じ2回の検索が行われ、`requests=2`、`tool_calls=2` で変化しなかった。回答内容も、LoRAは低ランク行列だけを学習するPEFT手法、QLoRAは量子化したベースモデルにLoRAを適用してメモリを節約する手法、という要点が保たれた。
- 気づき・疑問：エージェント全体の検索必須指示を削除しても、`search_glossary` のdocstringに「答える前に使うこと」「queryには用語を1つだけ入れる」と残っているため、モデルは引き続き2語を別々に検索したと考えられる。指示はINSTRUCTIONSだけでなく、ツールの説明文からも行動に影響することが分かった。確率的な挙動なので、複数回試すと違いが出る可能性はある。
