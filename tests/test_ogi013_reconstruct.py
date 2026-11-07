from runners.ogi013_reconstruct import classify, letter


def test_letter_takes_last_answer_line():
    assert letter("ANSWER: A ... then ANSWER: (C)") == "C" and letter("no answer") is None


def test_effect_is_measured_against_primary_and_key():
    f = {"p": "H", "o": "B"}
    assert classify(f, "B", "B", "p") == "IMPROVED"
    assert classify({"p": "H"}, "G", "H", "p") == "DEGRADED"
    assert classify({"p": "H"}, "H", "H", "p") == "UNCHANGED_RIGHT"
    assert classify({"p": "H"}, "H", "A", "p") == "UNCHANGED_WRONG"
    assert classify({"a": "A", "b": "F"}, "F", "F", None) == "RIGHT_ANSWER_PRESENT_FROM_START"
    assert classify({"a": "A", "b": "B"}, "F", "F", None) == "IMPROVED_OVER_BOTH_FIRST_ANSWERS"
