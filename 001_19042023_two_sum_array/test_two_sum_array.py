from main import twoSum


def test_two_sum_array_1():
    assert twoSum([2, 7, 11, 15], 9) == [0, 1]


def test_two_sum_array_2():
    assert twoSum([3, 2, 4], 6) == [1, 2]


def test_two_sum_array_3():
    assert twoSum([3, 3], 6) == [0, 1]
