from .config import Config
from .intents import Intent, detect_intent
from .prompts import SELF_TEST_OFFER, SYSTEM_PROMPT
from .resources import (
    CRISIS_MESSAGE,
    format_counseling_services,
    format_protection_tools,
)

INTENT_CONTEXT = {
    Intent.SELF_TEST: (
        "Die Person zeigt Interesse an einem Selbsttest. Weise empathisch darauf hin, "
        "dass der anonyme PGSI-Selbsttest jederzeit mit /selbsttest (oder auf zusagliche "
        "Aufforderung) gestartet werden kann, und biete an, danach gemeinsam uber das "
        f"Ergebnis zu sprechen. Zusatzangebot: {SELF_TEST_OFFER}"
    ),
    Intent.PROTECTION_TOOLS: (
        "Die Person fragt nach Spielerschutz-Tools. Integriere diese Informationen "
        "natürlich und empathisch in deine Antwort:\n" + format_protection_tools()
    ),
    Intent.COUNSELING: (
        "Die Person sucht Beratung oder Hilfsangebote. Integriere diese Angebote "
        "warm und ohne Druck in deine Antwort:\n" + format_counseling_services()
    ),
}


class ChatSession:
    def __init__(self, client, config: Config) -> None:
        self._client = client
        self._config = config
        self._messages: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]

    @property
    def messages(self) -> list[dict]:
        return [dict(message) for message in self._messages]

    def clear(self) -> None:
        self._messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def _trim_history(self) -> None:
        limit = self._config.max_history_messages
        if len(self._messages) > limit + 1:
            self._messages = [self._messages[0]] + self._messages[-(limit):]

    def send(self, text: str) -> str:
        intent = detect_intent(text)
        if intent == Intent.CRISIS:
            self._messages.append({"role": "user", "content": text})
            self._messages.append({"role": "assistant", "content": CRISIS_MESSAGE})
            self._trim_history()
            return CRISIS_MESSAGE

        self._messages.append({"role": "user", "content": text})
        call_messages = list(self._messages)
        if intent in INTENT_CONTEXT:
            call_messages.append({"role": "system", "content": INTENT_CONTEXT[intent]})
        reply = self._client.complete(call_messages)
        self._messages.append({"role": "assistant", "content": reply})
        self._trim_history()
        return reply
