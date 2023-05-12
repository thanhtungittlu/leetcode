from main import singleNumber


def test_1():
    assert singleNumber([2, 2, 1]) == 1


def test_2():
    assert singleNumber([4, 1, 2, 1, 2]) == 4


def test_3():
    assert singleNumber([1]) == 1
