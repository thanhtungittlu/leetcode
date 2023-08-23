from collections import Counter, OrderedDict


def reorganizeString(s):
    """
    :type s: str
    :rtype: str
    """
    dictS = dict(Counter(s))
    res =  max(dictS, key=lambda k: dictS[k])
    s = s.replace(res,"",1)
    while len(s) > 0:
        char = max(dictS, key=lambda k: dictS[k])
        if char == res[-1]:
            del dictS[char]
            if not dictS:
                return ""
        else:
            res = res + char
            s = s.replace(char, "", 1)
            dictS = dict(Counter(s))
    return res

s = "aabbcc"
print(reorganizeString(s))


