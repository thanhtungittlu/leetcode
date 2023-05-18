from main import sortedSquares


def test_1():
    assert sortedSquares([-4, -1, 0, 3, 10]) == [0, 1, 9, 16, 100]


def test_2():
    assert sortedSquares([-7, -3, 2, 3, 11]) == [4, 9, 9, 49, 121]
