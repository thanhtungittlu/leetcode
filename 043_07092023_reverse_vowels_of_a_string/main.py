def reverseVowels(s):
    """
    :type s: str
    :rtype: str
    """
    vowels = ['u', 'e', 'o', 'a', 'i', 'U', 'E', 'O', 'A', 'I']
    arrayS = list(s)
    left = 0
    right = len(arrayS) - 1
    while left <= right:
        isReverse = False
        if arrayS[left] in vowels:
            while isReverse == False:
                if arrayS[right] in vowels:
                    arrayS[left], arrayS[right] = arrayS[right], arrayS[left]
                    isReverse = True
                right -= 1   
                if right == left:
                    break
        left += 1
    res = ''.join(arrayS)
    return res


s = "hello"
print(reverseVowels(s))