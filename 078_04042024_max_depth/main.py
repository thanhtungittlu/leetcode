# def maxDepth(s: str) -> int:
#     res = 0
#     cur = 0
#     arr = []
#     is_close = False
#     for c in s:
#         if c == "(":
#             arr.append(c)
#             if is_close:
#                 cur = 0
#         elif c == ")":
#             cur += 1
#             arr.remove("(")
#             is_close = True
#         else:
#             continue
#         if not arr:
#             res = max(res, cur)
#             cur = 0
#     return res


def maxDepth(s: str) -> int:
    max_depth = 0
    current_depth = 0

    for c in s:
        if c == '(':
            current_depth += 1
            max_depth = max(max_depth, current_depth)
        elif c == ')':
            if current_depth > 0:
                current_depth -= 1

    return max_depth


s = "(()+((())))+((0))+(((())))"
print(maxDepth(s))
