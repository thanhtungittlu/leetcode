def lengthOfLastWord(s):
    """
    :type s: str
    :rtype: int
    """
    return len(s.split()[-1])


s = "   fly me   to   the moon  "
print(lengthOfLastWord(s))