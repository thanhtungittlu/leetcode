def isValid(string):
    stack = []
    dict_parenthese = {
        ")": "(",
        "]": "[",
        "}": "{"
    }
    for char in string:
        if char in dict_parenthese:
            last_ele = stack.pop() if stack else ""
            if last_ele != dict_parenthese[char]:
                return False
        else:
            stack.append(char)

    return not stack

s = "([])"
print(isValid(s))