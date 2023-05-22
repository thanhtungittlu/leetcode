# def findTheDifference(s, t):
#     """
#     :type s: str
#     :type t: str
#     :rtype: str
#     """
#     arrS = sorted(list(s))
#     arrT = sorted(list(t))
#     for i in range(len(arrS)):
#         print(arrS[i])
#         print(arrT[i])
#         if arrS[i] != arrT[i]:
#             return arrT[i]
#         else:
#             continue
#     return arrT[-1]

def findTheDifference(s, t):
    """
    :type s: str
    :type t: str
    :rtype: str
    """
    for char in t:
        if s.count(char) != t.count(char):
            return char


findTheDifference("ae", "aea")
