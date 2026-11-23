import os

import streamlit as st
from dotenv import load_dotenv

from lumo_core import (
    KRISE_KEYWORDS,
    TEXT_BERATUNG,
    TEXT_SELBSTTEST_INTRO,
    TEXT_SOFORTHILFE,
    TEXT_SPIIELERSCHUTZ,
    LumoBot,
)
from selbsttest import PGSI_FRAGEN, PGSI_SKALA, antwort_parsen, auswertung

load_dotenv()

st.set_page_config(
    page_title="Lumo – Anonymer Spielerschutz-Chat",
    page_icon="💬",
    layout="centered",
)


def resolve_api_key() -> str:
    key = os.environ.get("MISTRAL_API_KEY", "")
    if not key:
        try:
            key = st.secrets.get("MISTRAL_API_KEY", "")
        except Exception:
            key = ""
    return key


@st.cache_resource
def get_bot(api_key: str, demo_mode: bool) -> LumoBot:
    return LumoBot(api_key=api_key or None, demo_mode=demo_mode)


def init_state():
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("selbsttest", None)
    st.session_state.setdefault("demo_mode", False)


def add_message(role: str, content: str):
    st.session_state.messages.append({"role": role, "content": content})


def selbsttest_frage(idx: int) -> str:
    return (
        f"**Frage {idx + 1} von {len(PGSI_FRAGEN)}:** {PGSI_FRAGEN[idx]}\n\n"
        f"Antworte mit: {', '.join(PGSI_SKALA)}"
    )


def start_selbsttest():
    st.session_state.selbsttest = {"antworten": []}
    add_message("assistant", TEXT_SELBSTTEST_INTRO + selbsttest_frage(0))


def handle_selbsttest_answer(text: str):
    parsed = antwort_parsen(text)
    if parsed == "abbruch":
        st.session_state.selbsttest = None
        add_message("assistant", "Alles klar, ich breche den Selbsttest ab. Nichts wurde gespeichert. "
                                 "Wenn du später nochmal starten möchtest, sag einfach „Selbsttest“.")
        return
    if parsed is None:
        add_message("assistant", "Bitte antworte mit einer Zahl von 0 bis 3: " + ", ".join(PGSI_SKALA))
        return
    state = st.session_state.selbsttest
    state["antworten"].append(parsed)
    n = len(state["antworten"])
    if n < len(PGSI_FRAGEN):
        add_message("assistant", selbsttest_frage(n))
    else:
        st.session_state.selbsttest = None
        score = sum(state["antworten"])
        add_message("assistant", f"Danke für deine Ehrlichkeit. ✅ Der Test ist fertig.\n\n" + auswertung(score))


def handle_user_text(text: str):
    add_message("user", text)
    if st.session_state.selbsttest is not None:
        handle_selbsttest_answer(text)
        return
    t = text.lower()
    if any(k in t for k in KRISE_KEYWORDS):
        add_message("assistant", TEXT_SOFORTHILFE)
        return
    if "selbsttest" in t or ("test" in t and any(w in t for w in ["machen", "starten", "spielverhalten", "pgsi"])):
        start_selbsttest()
        return
    if any(k in t for k in ["spielerschutz", "sperre", "oasis", "limit", "tool", "schutz", "pause", "ausschluss"]):
        add_message("assistant", TEXT_SPIIELERSCHUTZ)
        return
    if any(k in t for k in ["beratung", "beratungsstelle", "hilfe", "telefon", "hotline", "anlaufstelle", "nummer"]):
        add_message("assistant", TEXT_BERATUNG)
        return
    if any(k in t for k in ["soforthilfe", "krise", "notfall", "schlecht geht"]):
        add_message("assistant", TEXT_SOFORTHILFE)
        return
    api_key = resolve_api_key()
    demo = st.session_state.demo_mode or not api_key
    bot = get_bot(api_key, demo)
    history = [m for m in st.session_state.messages if m["role"] in ("user", "assistant")][-20:]
    try:
        reply = bot.chat(history)
    except Exception as exc:
        reply = (f"⚠️ Die Mistral-API hat gerade nicht geantwortet ({type(exc).__name__}). "
                 "Bitte prüfe deinen API-Key oder versuche es gleich noch einmal. "
                 "Bei akuten Sorgen erreichst du die TelefonSeelsorge unter 0800 111 0 111 (kostenfrei, anonym, rund um die Uhr).")
    add_message("assistant", reply)


init_state()

api_key = resolve_api_key()
if not api_key:
    st.session_state.demo_mode = True

with st.sidebar:
    st.title("💬 Lumo")
    st.caption("Anonymer Spielerschutz-Chat")
    st.info("🔒 **Vollständig anonym:** Dieses Gespräch wird nur in dieser Browser-Sitzung angezeigt und nirgends gespeichert. Es werden keine Daten abgefragt.")
    st.divider()
    if st.session_state.demo_mode:
        st.warning("⚠️ **Demo-Modus** – MISTRAL_API_KEY ist nicht gesetzt. Antworten kommen aus einem lokalen Fallback. Für echte Mistral-Antworten Key in `.env` eintragen (siehe README).")
    else:
        st.success("✅ Mistral-API verbunden")
    st.checkbox("Demo-Modus erzwingen (ohne API)", value=st.session_state.demo_mode,
                key="demo_mode", help="Nützlich zum Testen der Oberfläche ohne API-Key.")
    st.divider()
    if st.button("🔄 Neues Gespräch", use_container_width=True):
        st.session_state.messages = []
        st.session_state.selbsttest = None
        st.rerun()
    st.divider()
    st.caption("Lumo ersetzt keine medizinische oder psychologische Beratung.")

st.title("💬 Lumo – anonymer Spielerschutz-Chat")
st.caption("Ich bin Lumo. Ich höre dir zu – anonym, wertschätzend und ohne Vorurteile. Worum geht es dir heute?")

if not st.session_state.messages:
    add_message(
        "assistant",
        "Hallo! 👋 Ich bin Lumo. Du kannst mir alles rund um das Thema Glücksspiel und Spielverhalten "
        "erzählen – anonym und ohne judgement.\n\n"
        "Ich kann dir zum Beispiel helfen mit:\n"
        "- 🧪 einem **anonymen Selbsttest** (9 Fragen)\n"
        "- 🛡️ **Spielerschutz-Tools** (OASIS-Sperre, Limits, Spielpausen)\n"
        "- 📞 **Beratungsstellen** (kostenlos & anonym)\n\n"
        "Was beschäftigt dich gerade?",
    )

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

cols = st.columns(4)
with cols[0]:
    if st.button("🧪 Selbsttest", use_container_width=True):
        if st.session_state.selbsttest is None:
            add_message("user", "Ich möchte den anonymen Selbsttest machen.")
            start_selbsttest()
        else:
            add_message("assistant", "Der Selbsttest läuft bereits – beantworte bitte die aktuelle Frage mit 0–3.")
        st.rerun()
with cols[1]:
    if st.button("🛡️ Spielerschutz", use_container_width=True):
        add_message("user", "Welche Spielerschutz-Tools gibt es?")
        add_message("assistant", TEXT_SPIIELERSCHUTZ)
        st.rerun()
with cols[2]:
    if st.button("📞 Beratung", use_container_width=True):
        add_message("user", "Wo bekomme ich Beratung und Hilfe?")
        add_message("assistant", TEXT_BERATUNG)
        st.rerun()
with cols[3]:
    if st.button("🆘 Soforthilfe", use_container_width=True):
        add_message("user", "Soforthilfe")
        add_message("assistant", TEXT_SOFORTHILFE)
        st.rerun()

prompt = st.chat_input("Schreib Lumo … (anonym, es wird nichts gespeichert)")
if prompt:
    handle_user_text(prompt)
    st.rerun()
