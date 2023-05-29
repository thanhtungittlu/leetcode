from main import singleNumber


def test_1():
    assert singleNumber([1, 2, 1, 3, 2, 5]) == [3, 5]


def test_2():
    assert singleNumber([-1, 0]) == [-1, 0]
