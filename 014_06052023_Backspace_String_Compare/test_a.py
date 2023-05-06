from main import backspaceCompare


def test_1():
    assert backspaceCompare("ab#c", "ad#c") == True


def test_2():
    assert backspaceCompare("abc", "abc") == True


def test_3():
    assert backspaceCompare("a#c", "b") == False


def test_4():
    assert backspaceCompare("ab##", "c#d#") == True


def test_5():
    assert backspaceCompare("y#fo##f", "y#f#o##f") == True
