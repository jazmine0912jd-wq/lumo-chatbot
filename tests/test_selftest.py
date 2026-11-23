import pytest

from lumo.selftest import (
    MAX_SCORE,
    QUESTIONS,
    SelfTest,
    classify,
    parse_answer,
    score_answers,
)


def test_nine_questions():
    assert len(QUESTIONS) == 9
    assert MAX_SCORE == 27


def test_all_never_is_no_risk():
    result = score_answers([0] * 9)
    assert result.score == 0
    assert "kein" in result.category


@pytest.mark.parametrize("score", [1, 2])
def test_low_risk_boundaries(score):
    category, _ = classify(score)
    assert category == "geringes Risiko"


@pytest.mark.parametrize("score", [3, 7])
def test_moderate_risk_boundaries(score):
    category, _ = classify(score)
    assert category == "mittleres Risiko"


@pytest.mark.parametrize("score", [8, 27])
def test_problematic_boundaries(score):
    category, interpretation = classify(score)
    assert category == "problematisches Spielverhalten"
    assert "0800 1 37 27 00" in interpretation


def test_wrong_number_of_answers_raises():
    with pytest.raises(ValueError):
        score_answers([0] * 8)


def test_invalid_answer_value_raises():
    with pytest.raises(ValueError):
        score_answers([0] * 8 + [4])


def test_summary_mentions_anonymity_and_no_diagnosis():
    result = score_answers([0] * 9)
    summary = result.summary()
    assert "anonym" in summary
    assert "keine" in summary and "Diagnose" in summary


def test_parse_answer_accepts_words_and_numbers():
    assert parse_answer("nie") == 0
    assert parse_answer("Manchmal") == 1
    assert parse_answer(" meistens ") == 2
    assert parse_answer("fast immer") == 3
    assert parse_answer("2") == 2
    assert parse_answer("vielleicht") is None
    assert parse_answer("5") is None


def test_run_collects_answers_and_reasks_on_invalid_input():
    inputs = iter(["unsinn", "0", "1", "2", "3", "0", "0", "0", "0", "0"])
    outputs: list[str] = []
    result = SelfTest().run(input_fn=lambda prompt: next(inputs), output_fn=outputs.append)
    assert result.score == 6
    assert result.category == "mittleres Risiko"
    assert any("Bitte antworte" in line for line in outputs)
    assert any("Ergebnis: 6 von 27" in line for line in outputs)
