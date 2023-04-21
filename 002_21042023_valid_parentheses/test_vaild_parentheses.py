from main import isValid


def test_vaild_parenthese():
    assert isValid("()") == True
    assert isValid("()[]{}") == True
    assert isValid("(]") == False
    assert isValid("([])") == True
    assert isValid("a(]") == False
