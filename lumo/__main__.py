import sys

from .chat import ChatSession
from .client import MistralChatClient
from .config import load_config
from .prompts import HELP_MESSAGE, WELCOME_MESSAGE
from .resources import format_counseling_services, format_protection_tools
from .selftest import SelfTest

EXIT_WORDS = {"/quit", "/exit", "quit", "exit", "tschuss", "tschüss", "bye", "ciao"}


def safe_send(session: ChatSession, text: str) -> str:
    try:
        return session.send(text)
    except Exception:
        return (
            "Entschuldigung, da ist gerade etwas schiefgelaufen (API nicht erreichbar). "
            "Bitte prüfe deinen MISTRAL_API_KEY in der .env-Datei. Du kannst es danach "
            "gerne erneut versuchen."
        )


def run_chat() -> None:
    config = load_config()
    client = MistralChatClient(config)
    session = ChatSession(client, config)

    print(WELCOME_MESSAGE)
    print()

    while True:
        try:
            text = input("Du: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nLumo: Danke, dass du da warst. Pass auf dich auf. Bis bald!")
            break
        if not text:
            continue
        if text.lower() in EXIT_WORDS:
            print("Lumo: Danke, dass du da warst. Pass auf dich auf. Bis bald!")
            break

        command = text.lower()
        if command in {"/hilfe", "/help", "?"}:
            print("Lumo:", HELP_MESSAGE)
        elif command == "/selbsttest":
            result = SelfTest().run()
            reply = safe_send(
                session,
                "Die Person hat soeben den anonymen PGSI-Selbsttest abgeschlossen: "
                f"{result.score} von 27 Punkten, Kategorie: {result.category}. "
                "Bitte antworte empathisch, erklaere das Ergebnis in eigenen Worten und "
                "schlage passende naechste Schritte vor. Stelle klar, dass es keine "
                "Diagnose ist und Beratung moeglich ist.",
            )
            print("Lumo:", reply)
            print()
        elif command == "/tools":
            print("Lumo: Hier sind wichtige Spielerschutz-Tools:\n")
            print(format_protection_tools())
            print()
        elif command == "/beratung":
            print("Lumo: Diese Angebote sind kostenlos und anonym:\n")
            print(format_counseling_services())
            print()
        elif command == "/clear":
            session.clear()
            print("Lumo: Der bisherige Gesprächsverlauf wurde im Arbeitsspeicher gelöscht.")
        else:
            reply = safe_send(session, text)
            print("Lumo:", reply)
            print()


def main() -> int:
    try:
        run_chat()
    except SystemExit as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
