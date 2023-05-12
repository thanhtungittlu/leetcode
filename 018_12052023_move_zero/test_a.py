from main import moveZeroes


def test_1():
    assert moveZeroes([0, 1, 0, 3, 12]) == [1, 3, 12, 0, 0]


def test_2():
    assert moveZeroes([0]) == [0]


def test_3():
    assert moveZeroes([0, 0, 0, 1, 0, 3]) == [1, 3, 0, 0, 0, 0]
