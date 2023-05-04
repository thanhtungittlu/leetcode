from main import romanToInt


def test_1():
    assert romanToInt("III") == 3


def test_2():
    assert romanToInt("LVIII") == 58


def test_3():
    assert romanToInt("MCMXCIV") == 1994


def test_4():
    assert romanToInt("MMMDCCCLXXXVIII") == 3888
