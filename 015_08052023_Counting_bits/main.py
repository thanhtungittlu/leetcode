def countBits(n):
    """
    :type n: int
    :rtype: List[int]
    """
    result = []
    for i in range(n+1):
        binary_string = format(i, "b") 
        sum_binary = binary_string.count("1")
        result.append(sum_binary)

    return result
