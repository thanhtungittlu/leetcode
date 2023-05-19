from main import merge


def test_1():
    assert merge([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3) == [1, 2, 2, 3, 5, 6]


def test_2():
    assert merge([1], 1, [], 0) == [1]


def test_3():
    assert merge([0], 0, [1], 1) == [1]
