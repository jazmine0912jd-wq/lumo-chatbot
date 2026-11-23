from enum import Enum


class Intent(str, Enum):
    CRISIS = "crisis"
    SELF_TEST = "self_test"
    PROTECTION_TOOLS = "protection_tools"
    COUNSELING = "counseling"
    OTHER = "other"


CRISIS_KEYWORDS = (
    "suizid",
    "selbstmord",
    "umbringen",
    "nicht mehr leben",
    "leben nicht mehr",
    "will sterben",
    "tot sein",
    "mir das leben nehmen",
    "selbstverletz",
    "mich umbringen",
)

SELF_TEST_KEYWORDS = (
    "selbsttest",
    "selbst test",
    "fragebogen",
    "pgsi",
    "test machen",
    "hab ich ein problem",
    "habe ich ein problem",
    "spielproblem",
    "wie schlimm",
)

PROTECTION_TOOLS_KEYWORDS = (
    "sperr",
    "oasis",
    "lugas",
    "limit",
    "einzahl",
    "panik",
    "spielpause",
    "time-out",
    "timeout",
    "blockier",
    "betblocker",
    "gamban",
    "reality check",
    "spielerschutz",
    "schutz vor dem spiel",
    "weniger spielen",
    "aufhören",
    "stoppen",
)

COUNSELING_KEYWORDS = (
    "beratung",
    "beratungsstelle",
    "anlaufstelle",
    "hotline",
    "telefonnummer",
    "telefon",
    "therapie",
    "therapeut",
    "arzt",
    "klinik",
    "wer hilft",
    "wer kann mir helfen",
    "suchtberatung",
    "hilfe bekomme",
    "ansprechpartner",
)


def detect_intent(text: str) -> Intent:
    normalized = text.lower()
    if any(keyword in normalized for keyword in CRISIS_KEYWORDS):
        return Intent.CRISIS
    if any(keyword in normalized for keyword in SELF_TEST_KEYWORDS):
        return Intent.SELF_TEST
    if any(keyword in normalized for keyword in PROTECTION_TOOLS_KEYWORDS):
        return Intent.PROTECTION_TOOLS
    if any(keyword in normalized for keyword in COUNSELING_KEYWORDS):
        return Intent.COUNSELING
    return Intent.OTHER
