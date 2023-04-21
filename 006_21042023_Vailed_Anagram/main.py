# def isAnagram(s, t):
#     """
#     :type s: str
#     :type t: str
#     :rtype: bool
#     """
#     return sorted(s) == sorted(t)


def isAnagram(s, t):
    """
    :type s: str
    :type t: str
    :rtype: bool
    """
    if len(s) != len(t):
        return False
    for char in set(s):
        if s.count(char) != t.count(char):
            return False
    return True
