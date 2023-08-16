def maximum69Number(num):
    """
    :type num: int
    :rtype: int
    """
    res = str(num).replace("6","9",1)
    return int(res)

print(maximum69Number(9669))