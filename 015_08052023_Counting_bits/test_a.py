from main import countBits


def test_1():
    assert countBits(2) == [0, 1, 1]


def test_2():
    assert countBits(5) == [0, 1, 1, 2, 1, 2]
