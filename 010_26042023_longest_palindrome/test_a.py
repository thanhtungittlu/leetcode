from main import longestPalindrome


def test_1():
    assert longestPalindrome("abccccdd") == 7


def test_2():
    assert longestPalindrome("a") == 1

def test_3():
    assert longestPalindrome("ccc") == 3
