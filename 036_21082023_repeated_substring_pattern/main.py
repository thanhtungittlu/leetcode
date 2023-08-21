def repeatedSubstringPattern(s):
    """
    :type s: str
    :rtype: bool
    """
    lenS = len(s)

    for i in range(1,lenS // 2 +1):
        if lenS % i == 0:
            subSCheck = s[:i]
            if subSCheck * (lenS // i) == s:
                return True
    return False

s = "abcaabcaabca"
print(repeatedSubstringPattern(s))