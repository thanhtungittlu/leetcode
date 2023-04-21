from main import maxProfit


def test_vaild_parenthese():
    assert maxProfit([7, 1, 5, 3, 6, 4]) == 5
    assert maxProfit([7, 6, 4, 3, 1]) == 0
    assert maxProfit([7, 6, 4, 10, 3, 1, 4]) == 6
