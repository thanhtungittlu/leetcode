def minRemoveToMakeValid(s: str) -> str:
    dict_v = {
        "(": 0,
        ")": 0
    }
    new = ""
    for c in s:
        if c == "(":
            dict_v["("] += 1
            new += c
        elif c == ")":
            if dict_v[")"] == dict_v["("]:
                continue
            else:
                dict_v[")"] += 1
                new += c
        else:
            new += c
    while dict_v["("] - dict_v[")"] > 0:
        f_index = new.rfind("(")
        new = new[:f_index] + new[f_index + 1:]
        dict_v["("] -= 1
    return new


# Cách 2
def minRemoveToMakeValid_v2(s: str) -> str:
    arr = []
    new = ""
    for c in s:
        if c == "(":
            arr.append(c)
            new += c
        elif c == ")":
            if not arr:
                continue
            else:
                arr.pop()
                new += c
        else:
            new += c
    while arr:
        f_index = new.rfind("(")
        new = new[:f_index] + new[f_index + 1:]
        arr.pop()
    return new


s = "())()((("

print(minRemoveToMakeValid(s))
