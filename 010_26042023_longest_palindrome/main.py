def longestPalindrome(s):
    """
    :type s: str
    :rtype: int
    """
    char_to_count = {}
    for char in s:
        if char not in char_to_count:
            char_to_count[char] = 1
        else:
            char_to_count[char] += 1

    result = 0
    flag = False
    for _, value in char_to_count.items():
        if value % 2 == 0:
            result += value
        else:
            if value == 1:
                flag = True
            else:
                flag = True
                result += value - 1
    if flag:
        result += 1

    return result


longestPalindrome("Aabacacccdd")
