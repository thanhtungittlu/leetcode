def removeStars(s):
    """
    :type s: str
    :rtype: str
    """
    new_s = []
    for char in s:
        if char != "*":
            new_s.append(char)
        else:
            new_s.pop()

    return ''.join(new_s)

s = "leet**cod*e"
# Output: "lecoe"
print(removeStars(s))