from types import SimpleNamespace

from app import ask


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        usage_metadata=SimpleNamespace(prompt_token_count=12, candidates_token_count=34),
        text="回答",
    )

    class FakeChat:
        def send_message(self, question):
            return response

    assert ask.ask(FakeChat(), "質問") == "回答"
    assert "入力: 12, 出力: 34" in capsys.readouterr().out


def test_ask_reports_unknown_counts_when_usage_metadata_is_missing(monkeypatch, capsys):
    response = SimpleNamespace(usage_metadata=None, text="回答")

    class FakeChat:
        def send_message(self, question):
            return response

    ask.ask(FakeChat(), "質問")
    assert "入力: 不明, 出力: 不明" in capsys.readouterr().out


def test_main_keeps_conversation_history_until_quit(monkeypatch, capsys):
    questions = []

    class FakeChat:
        def send_message(self, question):
            questions.append(question)
            return SimpleNamespace(
                usage_metadata=SimpleNamespace(prompt_token_count=1, candidates_token_count=2),
                text=f"{question}への回答",
            )

    chat = FakeChat()

    class FakeChats:
        def create(self, *, model):
            return chat

    class FakeClient:
        def __init__(self, *, api_key):
            self.chats = FakeChats()

    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(ask.genai, "Client", FakeClient)
    monkeypatch.setattr("sys.argv", ["app.ask", "最初の質問"])
    inputs = iter(["続きの質問", "q"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))

    ask.main()

    output = capsys.readouterr().out
    assert questions == ["最初の質問", "続きの質問"]
    assert "最初の質問への回答" in output
    assert "続きの質問への回答" in output