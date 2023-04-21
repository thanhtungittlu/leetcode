import re


def isPalindrome(string):
    """
    :type s: str
    :rtype: bool
    """
    # Tìm ra những ký tự không phải số  hoặc chữ, và thay thế  bằng ''
    # string_convert = re.sub(r'[^a-zA-Z0-9]', '', string.lower())
    string_convert = re.sub(r'[\W_]', '', string.lower())

    return string_convert == string_convert[::-1]


print(isPalindrome("ab_a"))
