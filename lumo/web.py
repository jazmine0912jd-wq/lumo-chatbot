import html
import secrets
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from pydantic import BaseModel

from .chat import ChatSession
from .client import MistralChatClient
from .config import Config, load_config
from .resources import COUNSELING_SERVICES, PROTECTION_TOOLS
from .selftest import ANSWER_SCALE, QUESTIONS, score_answers

STATIC_DIR = Path(__file__).parent / "static"
SESSION_COOKIE = "lumo_session"

PAGE_CSS = (
    "body{font-family:system-ui,sans-serif;max-width:720px;margin:2rem auto;padding:0 1rem;"
    "background:#f6f7fb;color:#1c1e26}"
    "h1{color:#3b4bd8}a{color:#3b4bd8}"
    ".box{background:#fff;border:1px solid #e3e5ee;border-radius:12px;padding:1rem;margin:1rem 0}"
    "#log{display:flex;flex-direction:column;gap:.5rem;min-height:200px}"
    ".msg{padding:.5rem .8rem;border-radius:10px;max-width:85%;white-space:pre-wrap}"
    ".user{align-self:flex-end;background:#dfe4ff}.bot{align-self:flex-start;background:#eef0f6}"
    "#bar{display:flex;gap:.5rem}input[type=text]{flex:1;padding:.6rem;border:1px solid #ccc;border-radius:8px}"
    "button{padding:.6rem 1rem;border:0;border-radius:8px;background:#3b4bd8;color:#fff;cursor:pointer}"
    "fieldset{border:1px solid #e3e5ee;border-radius:8px;margin:.8rem 0}"
    "label{display:inline-block;margin-right:1rem}"
    ".nav a{margin-right:1rem}pre{white-space:pre-wrap;background:#eef0f6;padding:.8rem;border-radius:8px}"
)


def page(title: str, body: str) -> str:
    return (
        "<!doctype html><html lang=\"de\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        f"<title>{html.escape(title)}</title><style>{PAGE_CSS}</style></head><body>"
        f"<h1>Lumo</h1><p class=\"nav\">"
        "<a href=\"/\">Chat</a><a href=\"/selbsttest\">Anonymer Selbsttest</a>"
        "<a href=\"/tools\">Spielerschutz-Tools</a><a href=\"/beratung\">Beratungsstellen</a></p>"
        f"<div class=\"box\">{body}</div>"
        "<p><small>Anonym: Dieses Gespräch wird nur im Arbeitsspeicher gehalten und nicht protokolliert.</small></p>"
        "</body></html>"
    )


def tools_page() -> str:
    items = "".join(
        f"<li><strong>{html.escape(t.name)}</strong>: {html.escape(t.description)}</li>"
        for t in PROTECTION_TOOLS
    )
    return page("Spielerschutz-Tools", f"<h2>Spielerschutz-Tools</h2><ul>{items}</ul>")


def counseling_page() -> str:
    items = []
    for s in COUNSELING_SERVICES:
        details = []
        if s.phone:
            details.append(f"Tel: {html.escape(s.phone)}")
        if s.hours:
            details.append(html.escape(s.hours))
        if s.website:
            details.append(html.escape(s.website))
        meta = f" ({', '.join(details)})" if details else ""
        items.append(
            f"<li><strong>{html.escape(s.name)}</strong>{meta}: {html.escape(s.description)}</li>"
        )
    return page(
        "Beratungsstellen",
        "<h2>Kostenlose &amp; anonyme Beratungsangebote</h2>"
        "<p>Bei akuter Gefahr: <strong>Notruf 112</strong></p>"
        f"<ul>{''.join(items)}</ul>",
    )


def selftest_form_page() -> str:
    fields = []
    for i, question in enumerate(QUESTIONS, start=1):
        options = "".join(
            f'<label><input type="radio" name="q{i}" value="{value}" required> {html.escape(word)}</label>'
            for word, value in ANSWER_SCALE
        )
        fields.append(
            f"<fieldset><legend>Frage {i}/{len(QUESTIONS)}: {html.escape(question)}</legend>{options}</fieldset>"
        )
    return page(
        "Anonymer Selbsttest",
        "<h2>Anonymer Selbsttest (PGSI)</h2>"
        "<p>9 Fragen zu den letzten 12 Monaten. Anonym, wird nicht gespeichert, "
        "keine Diagnose. Skala: 0 = nie, 1 = manchmal, 2 = meistens, 3 = fast immer.</p>"
        f'<form method="post" action="/selftest">{"".join(fields)}'
        '<button type="submit">Auswerten</button></form>',
    )


class ChatRequest(BaseModel):
    message: str


def create_app(client=None, config: Config | None = None) -> FastAPI:
    config = config or load_config()
    client = client or MistralChatClient(config)
    sessions: dict[str, ChatSession] = {}
    app = FastAPI(title="Lumo")

    def session_for(request: Request) -> tuple[str, ChatSession]:
        sid = request.cookies.get(SESSION_COOKIE)
        session = sessions.get(sid) if sid else None
        if session is None:
            sid = secrets.token_urlsafe(24)
            session = ChatSession(client, config)
            sessions[sid] = session
        return sid, session

    @app.get("/", response_class=HTMLResponse)
    def index():
        return FileResponse(STATIC_DIR / "index.html")

    @app.post("/api/chat")
    def chat(req: ChatRequest, request: Request):
        sid, session = session_for(request)
        reply = session.send(req.message)
        response = JSONResponse({"reply": reply, "session_id": sid})
        response.set_cookie(SESSION_COOKIE, sid, httponly=True, samesite="lax", max_age=86400)
        return response

    @app.get("/selftest", response_class=HTMLResponse)
    def selftest_form():
        return selftest_form_page()

    @app.post("/selftest", response_class=HTMLResponse)
    def selftest_submit(
        q1: int = Form(), q2: int = Form(), q3: int = Form(),
        q4: int = Form(), q5: int = Form(), q6: int = Form(),
        q7: int = Form(), q8: int = Form(), q9: int = Form(),
    ):
        try:
            result = score_answers([q1, q2, q3, q4, q5, q6, q7, q8, q9])
        except ValueError:
            return HTMLResponse(
                page("Selbsttest", "<p>Ungültige Antworten. Bitte jede Frage mit 0–3 beantworten.</p>"),
                status_code=400,
            )
        return page(
            "Selbsttest-Ergebnis",
            "<h2>Dein Ergebnis</h2>"
            f"<pre>{html.escape(result.summary())}</pre>"
            "<p><a href=\"/selbsttest\">Test wiederholen</a> · <a href=\"/\">Weiter zum Chat</a></p>",
        )

    @app.get("/tools", response_class=HTMLResponse)
    def tools():
        return tools_page()

    @app.get("/beratung", response_class=HTMLResponse)
    def counseling():
        return counseling_page()

    return app


def main() -> None:
    import uvicorn

    uvicorn.run(create_app(), host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
