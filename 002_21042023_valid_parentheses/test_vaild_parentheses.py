from main import isValid


def test_vaild_parenthese_1():
    assert isValid("()") == True


def test_vaild_parenthese_2():
    assert isValid("()[]{}") == True


def test_vaild_parenthese_3():
    assert isValid("(]") == False


def test_vaild_parenthese_4():
    assert isValid("([])") == True


def test_vaild_parenthese_5():
    assert isValid("a(]") == False
