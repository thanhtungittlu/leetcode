from main import maxSubArray


def test_1():
    assert maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6


def test_2():
    assert maxSubArray([1]) == 1


def test_3():
    assert maxSubArray([5, 4, -1, 7, 8]) == 23


def test_4():
    assert maxSubArray([-5, -4, -1, 0, -8]) == 0
