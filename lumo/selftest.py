from dataclasses import dataclass
from typing import Callable

QUESTIONS = (
    "Hast du jemals mehr Geld verspielt, als du dir leisten konntest?",
    "Musstest du jemals mit hoeheren Einsaetzen spielen, um dieselbe Aufregung zu erleben?",
    "Bist du jemals an einem anderen Tag zuruckgekehrt, um verlorenes Geld zuruckzugewinnen?",
    "Hast du jemals Geld geliehen oder etwas verkauft, um Geld zum Spielen zu bekommen?",
    "Hattest du jemals das Gefuhl, dass du ein Problem mit dem Glucksspiel haben konntest?",
    "Hat das Glucksspiel jemals gesundheitliche Probleme bei dir verursacht, einschliesslich Stress oder Angst?",
    "Hat dich jemals jemand wegen deines Spielverhaltens kritisiert oder dir gesagt, du hattest ein Glucksspielproblem - unabhangig davon, ob du das selbst so sahst?",
    "Hast du dich jemals schuldig gefuhlt wegen deiner Art zu spielen oder wegen der Folgen deines Spielens?",
    "Hat dein Glucksspiel jemals finanzielle Probleme fur deinen Haushalt verursacht?",
)

ANSWER_SCALE = (
    ("nie", 0),
    ("manchmal", 1),
    ("meistens", 2),
    ("fast immer", 3),
)

ANSWER_BY_WORD = {word: value for word, value in ANSWER_SCALE}
ANSWER_BY_VALUE = {value: word for word, value in ANSWER_SCALE}

MAX_SCORE = 3 * len(QUESTIONS)

CATEGORY_NO_RISK = "kein erhohtes Risiko erkennbar"
CATEGORY_LOW_RISK = "geringes Risiko"
CATEGORY_MODERATE_RISK = "mittleres Risiko"
CATEGORY_PROBLEMATIC = "problematisches Spielverhalten"

INTERPRETATIONS = {
    CATEGORY_NO_RISK: (
        "Dein Ergebnis zeigt aktuell kein erhohtes Risiko. Spielerschutz-Tools wie "
        "Limits und Spielpausen konnen trotzdem helfen, es dabei zu belassen."
    ),
    CATEGORY_LOW_RISK: (
        "Dein Ergebnis zeigt ein geringes Risiko. Feste Limits (Einzahlung, Zeit, "
        "Verluste) und regelmassige Reality Checks konnen helfen, die Kontrolle zu behalten."
    ),
    CATEGORY_MODERATE_RISK: (
        "Dein Ergebnis zeigt ein mittleres Risiko. Eine Spielpause, die Selbstsperre uber "
        "OASIS oder Sperrsoftware konnen jetzt sinnvolle nachste Schritte sein. Die "
        "BIÖG-Telefonberatung (0800 1 37 27 00, kostenlos und anonym) unterstutzt dich gerne."
    ),
    CATEGORY_PROBLEMATIC: (
        "Dein Ergebnis deutet auf ein problematisches Spielverhalten hin. Das ist keine "
        "Diagnose, aber ein wichtiges Signal. Bitte wende dich an eine Beratungsstelle - "
        "z. B. die BIÖG-Telefonberatung zur Glucksspielsucht unter 0800 1 37 27 00 "
        "(kostenlos, anonym, check-dein-spiel.de) oder eine Suchtberatungsstelle vor Ort. "
        "Eine Selbstsperre uber OASIS kann zusatzlich helfen. Du bist nicht allein."
    ),
}


@dataclass(frozen=True)
class SelfTestResult:
    score: int
    category: str
    interpretation: str

    def summary(self) -> str:
        return (
            f"Ergebnis: {self.score} von {MAX_SCORE} Punkten - {self.category}.\n"
            f"{self.interpretation}\n"
            "Hinweis: Dieser Selbsttest ist anonym, wird nicht gespeichert und ersetzt "
            "keine professionelle Diagnose oder Beratung."
        )


def classify(score: int) -> tuple[str, str]:
    if score <= 0:
        category = CATEGORY_NO_RISK
    elif score <= 2:
        category = CATEGORY_LOW_RISK
    elif score <= 7:
        category = CATEGORY_MODERATE_RISK
    else:
        category = CATEGORY_PROBLEMATIC
    return category, INTERPRETATIONS[category]


def score_answers(answers: list[int]) -> SelfTestResult:
    if len(answers) != len(QUESTIONS):
        raise ValueError(f"Es werden genau {len(QUESTIONS)} Antworten erwartet.")
    for answer in answers:
        if not isinstance(answer, int) or answer not in ANSWER_BY_VALUE:
            raise ValueError("Antworten mussen 0, 1, 2 oder 3 sein.")
    score = sum(answers)
    category, interpretation = classify(score)
    return SelfTestResult(score=score, category=category, interpretation=interpretation)


def parse_answer(raw: str) -> int | None:
    text = raw.strip().lower()
    if text in ANSWER_BY_WORD:
        return ANSWER_BY_WORD[text]
    if text in {str(value) for value in ANSWER_BY_VALUE}:
        return int(text)
    return None


class SelfTest:
    def run(
        self,
        input_fn: Callable[[str], str] = input,
        output_fn: Callable[[str], None] = print,
    ) -> SelfTestResult:
        from .prompts import SELF_TEST_INTRO

        output_fn(SELF_TEST_INTRO)
        answers: list[int] = []
        for index, question in enumerate(QUESTIONS, start=1):
            while True:
                raw = input_fn(f"Frage {index}/{len(QUESTIONS)}: {question} [0-3] ")
                answer = parse_answer(raw)
                if answer is None:
                    output_fn("Bitte antworte mit 0 (nie), 1 (manchmal), 2 (meistens) oder 3 (fast immer).")
                    continue
                answers.append(answer)
                break
        result = score_answers(answers)
        output_fn(result.summary())
        return result
