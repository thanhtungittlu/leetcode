from main import isPalindrome


def test_vaild_palindrome_1():
    assert isPalindrome("A man, a plan, a canal: Panama") == True


def test_vaild_palindrome_2():
    assert isPalindrome("race a car") == False


def test_vaild_palindrome_3():
    assert isPalindrome(" ") == True


def test_vaild_palindrome_4():
    assert isPalindrome("ab_a") == True
