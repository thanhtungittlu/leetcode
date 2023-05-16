from main import missingNumber


def test_1():
    assert missingNumber([3, 0, 1]) == 2


def test_2():
    assert missingNumber([0, 1]) == 2


def test_3():
    assert missingNumber([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8
