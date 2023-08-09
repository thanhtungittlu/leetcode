def reverse(x):
    """
    :type x: int
    :rtype: int
    """
    INT_MAX = 2**31 - 1
    INT_MIN = -2**31
    
    sign = 1 if x >= 0 else -1
    x = abs(x)
    
    int_reverse = int(str(x)[::-1]) * sign
    
    if INT_MIN <= int_reverse <= INT_MAX:
        return int_reverse
    else:
        return 0
    

print(2**31 - 1534236469)