from main import containsDuplicate


def test_1():
    assert containsDuplicate([1, 2, 3, 1]) == True


def test_2():
    assert containsDuplicate([1, 2, 3, 4]) == False


def test_3():
    assert containsDuplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) == True
