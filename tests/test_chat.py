from lumo.chat import ChatSession
from lumo.config import Config
from lumo.resources import CRISIS_MESSAGE


class FakeClient:
    def __init__(self):
        self.calls: list[list[dict]] = []

    def complete(self, messages: list[dict]) -> str:
        self.calls.append([dict(m) for m in messages])
        return "Fake-Antwort"


def make_session() -> tuple[ChatSession, FakeClient]:
    config = Config(api_key="test", max_history_messages=6)
    client = FakeClient()
    return ChatSession(client, config), client


def test_normal_message_calls_client_and_keeps_history():
    session, client = make_session()
    reply = session.send("Hallo Lumo")
    assert reply == "Fake-Antwort"
    assert len(client.calls) == 1
    roles = [m["role"] for m in session.messages]
    assert roles == ["system", "user", "assistant"]


def test_crisis_short_circuits_without_api_call():
    session, client = make_session()
    reply = session.send("ich will mich umbringen")
    assert reply == CRISIS_MESSAGE
    assert "0800 111 0 111" in reply
    assert client.calls == []
    roles = [m["role"] for m in session.messages]
    assert roles == ["system", "user", "assistant"]


def test_intent_injects_context_but_not_into_history():
    session, client = make_session()
    session.send("wie kann ich mich sperren lassen? OASIS")
    assert len(client.calls) == 1
    called = client.calls[0]
    assert any("OASIS" in m["content"] for m in called)
    assert called[-1]["role"] == "system"
    roles = [m["role"] for m in session.messages]
    assert roles == ["system", "user", "assistant"]


def test_clear_resets_history_to_system_prompt():
    session, _ = make_session()
    session.send("Hallo")
    session.clear()
    assert [m["role"] for m in session.messages] == ["system"]


def test_history_is_trimmed_to_limit():
    session, _ = make_session()
    for i in range(10):
        session.send(f"Nachricht {i}")
    assert len(session.messages) <= 7
    assert session.messages[0]["role"] == "system"
