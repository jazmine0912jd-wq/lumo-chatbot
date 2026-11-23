import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "mistral-small-latest"


@dataclass(frozen=True)
class Config:
    api_key: str
    model: str = DEFAULT_MODEL
    temperature: float = 0.7
    max_tokens: int = 900
    max_history_messages: int = 40


def load_config() -> Config:
    api_key = os.environ.get("MISTRAL_API_KEY", "").strip()
    if not api_key:
        raise SystemExit(
            "MISTRAL_API_KEY ist nicht gesetzt. Bitte .env anlegen "
            "(siehe .env.example) oder die Umgebungsvariable setzen."
        )
    return Config(
        api_key=api_key,
        model=os.environ.get("MISTRAL_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL,
        temperature=float(os.environ.get("LUMO_TEMPERATURE", "0.7")),
        max_tokens=int(os.environ.get("LUMO_MAX_TOKENS", "900")),
        max_history_messages=int(os.environ.get("LUMO_MAX_HISTORY", "40")),
    )
