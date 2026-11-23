from lumo.intents import Intent, detect_intent


def test_crisis_keywords():
    assert detect_intent("ich will mich umbringen") == Intent.CRISIS
    assert detect_intent("Gedanken vom Suizid") == Intent.CRISIS
    assert detect_intent("ich will nicht mehr leben") == Intent.CRISIS
    assert detect_intent("selbstverletzen") == Intent.CRISIS


def test_crisis_takes_precedence():
    assert detect_intent("ich brauche hilfe, ich will mich umbringen") == Intent.CRISIS


def test_self_test_intent():
    assert detect_intent("Kann ich einen Selbsttest machen?") == Intent.SELF_TEST
    assert detect_intent("Habe ich ein Problem mit Spielen? PGSI") == Intent.SELF_TEST


def test_protection_tools_intent():
    assert detect_intent("Wie kann ich mich bei OASIS sperren lassen?") == Intent.PROTECTION_TOOLS
    assert detect_intent("Gibt es ein Einzahlungslimit?") == Intent.PROTECTION_TOOLS
    assert detect_intent("Ich will aufhören zu spielen") == Intent.PROTECTION_TOOLS


def test_counseling_intent():
    assert detect_intent("Gibt es eine Beratungsstelle in meiner Nähe?") == Intent.COUNSELING
    assert detect_intent("Welche Telefonnummer hat die Suchtberatung?") == Intent.COUNSELING


def test_other_intent():
    assert detect_intent("Hallo, wie geht es dir?") == Intent.OTHER
    assert detect_intent("") == Intent.OTHER
