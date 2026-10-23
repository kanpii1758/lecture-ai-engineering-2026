from types import SimpleNamespace

from app import ask as ask_module


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        text="回答",
        usage_metadata=SimpleNamespace(prompt_token_count=12, candidates_token_count=7),
    )
    models = SimpleNamespace(
        generate_content=lambda **_: response,
    )
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(
        ask_module.genai,
        "Client",
        lambda **_: SimpleNamespace(models=models),
    )

    assert ask_module.ask("質問") == "回答"
    assert capsys.readouterr().out == "[usage] input=12 output=7\n"


def test_ask_reports_unavailable_token_usage(monkeypatch, capsys):
    response = SimpleNamespace(text="回答", usage_metadata=None)
    models = SimpleNamespace(
        generate_content=lambda **_: response,
    )
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(
        ask_module.genai,
        "Client",
        lambda **_: SimpleNamespace(models=models),
    )

    assert ask_module.ask("質問") == "回答"
    assert capsys.readouterr().out == "[usage] unavailable\n"
