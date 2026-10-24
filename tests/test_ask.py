from google.genai import types

from app import ask as ask_module


class FakeModels:
    def __init__(self):
        self.contents = None

    def generate_content(self, *, model, contents):
        self.contents = contents
        return type("Response", (), {"text": "回答"})()


class FakeClient:
    def __init__(self, api_key):
        self.models = FakeModels()


def test_ask_sends_typed_text_parts_and_updates_history(monkeypatch):
    client = FakeClient(api_key="test-key")
    monkeypatch.setattr(ask_module.genai, "Client", lambda **kwargs: client)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    history = [{"role": "user", "text": "前の質問"}, {"role": "model", "text": "前の回答"}]

    response, updated_history = ask_module.ask("LoRAとは何ですか？", history)

    assert response == "回答"
    assert all(isinstance(content, types.Content) for content in client.models.contents)
    assert [
        (content.role, content.parts[0].text) for content in client.models.contents
    ] == [
        ("user", "前の質問"),
        ("model", "前の回答"),
        ("user", "LoRAとは何ですか？"),
    ]
    assert updated_history == [
        {"role": "user", "text": "前の質問"},
        {"role": "model", "text": "前の回答"},
        {"role": "user", "text": "LoRAとは何ですか？"},
        {"role": "model", "text": "回答"},
    ]


def test_first_question_is_sent_as_user_content(monkeypatch):
    client = FakeClient(api_key="test-key")
    monkeypatch.setattr(ask_module.genai, "Client", lambda **kwargs: client)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")

    ask_module.ask("LoRAとは何ですか？", [])

    assert len(client.models.contents) == 1
    content = client.models.contents[0]
    assert isinstance(content, types.Content)
    assert content.role == "user"
    assert content.parts[0].text == "LoRAとは何ですか？"


def test_ask_sends_text_in_sdk_request_body(monkeypatch):
    client = ask_module.genai.Client(api_key="test-key")
    request = {}

    def fake_request(method, path, body, http_options=None):
        request.update(method=method, path=path, body=body)
        return types.HttpResponse(
            headers={},
            body='{"candidates":[{"content":{"parts":[{"text":"回答"}],"role":"model"},"finishReason":"STOP"}]}',
        )

    monkeypatch.setattr(client._api_client, "request", fake_request)
    monkeypatch.setattr(ask_module.genai, "Client", lambda **kwargs: client)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")

    response, _ = ask_module.ask("LoRAとは何ですか？", [])

    assert response == "回答"
    assert request["body"]["contents"] == [
        {
            "parts": [{"text": "LoRAとは何ですか？"}],
            "role": "user",
        }
    ]
