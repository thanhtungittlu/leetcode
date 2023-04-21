def isValid(string):
    stack = []
    mapping = {
        ")": "(",
        "]": "[",
        "}": "{",
    }
    for char in string:
        if char in mapping:
            last_element = stack.pop() if stack else ""
            if last_element != mapping[char]:
                return False
        else:
            stack.append(char)
    return not stack


str1 = "()"
str2 = "()[]{}"
str3 = "(]"
str4 = "([])"

print(isValid(str1))
print(isValid(str2))
print(isValid(str3))
print(isValid(str4))
