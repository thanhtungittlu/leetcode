from main import maxProfit


def test_vaild_parenthese_1():
    assert maxProfit([7, 1, 5, 3, 6, 4]) == 5


def test_vaild_parenthese_2():
    assert maxProfit([7, 6, 4, 3, 1]) == 0


def test_vaild_parenthese_3():
    assert maxProfit([7, 6, 4, 10, 3, 1, 4]) == 6
