def remove_hastag(string):
    arr_str = list(string)
    while "#" in arr_str:
        pos = arr_str.index("#")
        arr_str.pop(pos)
        if pos != 0:
            arr_str.pop(pos-1)

    return str(arr_str)


def backspaceCompare(s, t):
    """
    :type s: str
    :type t: str
    :rtype: bool
    """
    return remove_hastag(s) == remove_hastag(t)


print(remove_hastag("#f"))

# def backspaceCompare(s, t):
#     c = []
#     d = []

#     for x in s:
#         if x != '#':
#             c.append(x)
#         else:
#             if c:
#                 c.pop()

#     for x in t:
#         if x != '#':
#             d.append(x)
#         else:
#             if d:
#                 d.pop()

#     return (c==d)
