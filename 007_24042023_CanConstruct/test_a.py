from main import canConstruct


def test_1():
    assert canConstruct("a", "b") == False


def test_2():
    assert canConstruct("aa", "ab") == False


def test_3():
    assert canConstruct("aa", "aab") == True


def test_4():
    assert canConstruct("aab", "baa") == True
