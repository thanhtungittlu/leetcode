from main import findTheDifference


def test_1():
    assert findTheDifference("abcd", "abcde") == "e"


def test_2():
    assert findTheDifference("", "y") == "y"


def test_2():
    assert findTheDifference("ae", "aea") == "a"
