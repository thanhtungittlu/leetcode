from main import longestCommonPrefix


def test_1():
    assert longestCommonPrefix(["flower","flow","flight"]) == "fl"


def test_2():
    assert longestCommonPrefix(["dog","racecar","car"]) == ""


