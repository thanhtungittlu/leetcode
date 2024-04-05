def makeGood(s: str) -> str:
    result = []
    for char in s:
        if result and char.swapcase() == result[-1]:
            result.pop()
        else:
            result.append(char)
    return ''.join(result)


s = "leEeetcode"
print(makeGood(s))
