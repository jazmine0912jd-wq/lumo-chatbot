from fastapi.testclient import TestClient

from lumo.config import Config
from lumo.web import create_app


class FakeClient:
    def __init__(self):
        self.calls: list[list[dict]] = []

    def complete(self, messages: list[dict]) -> str:
        self.calls.append([dict(m) for m in messages])
        return "Fake-Antwort"


def make_client() -> tuple[TestClient, FakeClient]:
    fake = FakeClient()
    app = create_app(client=fake, config=Config(api_key="test"))
    return TestClient(app), fake


def test_index_page():
    client, _ = make_client()
    response = client.get("/")
    assert response.status_code == 200
    assert "Lumo" in response.text


def test_chat_roundtrip_sets_session_cookie():
    client, fake = make_client()
    response = client.post("/api/chat", json={"message": "Hallo Lumo"})
    assert response.status_code == 200
    data = response.json()
    assert data["reply"] == "Fake-Antwort"
    assert "lumo_session" in response.cookies
    assert len(fake.calls) == 1

    response2 = client.post("/api/chat", json={"message": "Und jetzt?"})
    assert len(fake.calls) == 2
    assert response2.json()["session_id"] == data["session_id"]


def test_crisis_message_short_circuits_without_api_call():
    client, fake = make_client()
    response = client.post("/api/chat", json={"message": "ich will mich umbringen"})
    assert response.status_code == 200
    assert "0800 111 0 111" in response.json()["reply"]
    assert fake.calls == []


def test_selftest_form_page():
    client, _ = make_client()
    response = client.get("/selftest")
    assert response.status_code == 200
    assert "Frage 1/9" in response.text
    assert "Frage 9/9" in response.text


def test_selftest_submit_max_score():
    client, _ = make_client()
    data = {f"q{i}": "3" for i in range(1, 10)}
    response = client.post("/selftest", data=data)
    assert response.status_code == 200
    assert "27 von 27 Punkten" in response.text
    assert "problematisches Spielverhalten" in response.text
    assert "0800 1 37 27 00" in response.text


def test_selftest_submit_invalid_answer_returns_400():
    client, _ = make_client()
    data = {f"q{i}": "0" for i in range(1, 10)}
    data["q9"] = "9"
    response = client.post("/selftest", data=data)
    assert response.status_code == 400


def test_tools_page_lists_oasis_and_lugas():
    client, _ = make_client()
    response = client.get("/tools")
    assert response.status_code == 200
    assert "OASIS" in response.text
    assert "LUGAS" in response.text


def test_counseling_page_lists_hotlines():
    client, _ = make_client()
    response = client.get("/beratung")
    assert response.status_code == 200
    assert "0800 1 37 27 00" in response.text
    assert "0800 111 0 111" in response.text
    assert "112" in response.text
