def rangeBitwiseAnd(left, right):
    """
    :type left: int
    :type right: int
    :rtype: int
    """
    shift = 0

    while left < right:
        left >>= 1
        right >>= 1
        shift += 1

    return left << shift

print(rangeBitwiseAnd(5, 7))