from main import combinationSum


def test_1():
    assert combinationSum([2,3,6,7], 7) == [[2,2,3],[7]]


def test_2():
    assert combinationSum([2,3,5], 8) == [[2,2,2,2],[2,3,3],[3,5]]

