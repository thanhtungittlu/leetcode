def isAnagram(s, t):
    """
    :type s: str
    :type t: str
    :rtype: bool
    """
    if len(s) != len(t):
        return False
    
    dictS = {}
    for char in s:
        if char not in dictS:
            dictS[char] = 1
        else:
            dictS[char] += 1

    for char in t:
        if char not in dictS:
            return False
        
        if dictS[char] != t.count(char):
            return False
    
    return True

s = "ab"
t = "aab"

print(isAnagram(s, t))