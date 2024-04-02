def isIsomorphic(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    dict_m_s = {}
    for i, value in enumerate(s):
        if value not in dict_m_s:
            dict_m_s[value] = t[i]
        else:
            if dict_m_s[value] != t[i]:
                return False
    dict_m_t = {}
    for i, value in enumerate(t):
        if value not in dict_m_t:
            dict_m_t[value] = s[i]
        else:
            if dict_m_t[value] != s[i]:
                return False
    return True


s = "badc"
t = "baba"
print(isIsomorphic(s, t))
