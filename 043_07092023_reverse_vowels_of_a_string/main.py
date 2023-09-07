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
        if arrayS[left] in vowels:
            if arrayS[right] in vowels:
                arrayS[left],arrayS[right] = arrayS[right],arrayS[left]
                left+=1
                right-=1
            else:
                right-=1
        else:
            left+=1
    return ''.join(arrayS)


s = "hello"
print(reverseVowels(s))