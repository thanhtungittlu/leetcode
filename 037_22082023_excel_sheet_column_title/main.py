def convertToTitle(columnNumber):
    """
    :type columnNumber: int
    :rtype: str
    """
    title = ""
    while columnNumber > 0:
        columnNumber -= 1 #Vì index của excel đánh từ 1
        title = chr(columnNumber % 26 + ord('A')) + title
        columnNumber //= 26
    
    return title

columnNumber = 721
print(convertToTitle(columnNumber))