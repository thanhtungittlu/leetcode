def myPow(x, n):
    """
    :type x: float
    :type n: int
    :rtype: float
    """
    if n == 0:
        return 1
    if n < 0:
        x = 1 / x
        n = -n

    half_pow = myPow(x, n // 2)
    
    if n % 2 == 0:
        return half_pow * half_pow
    else:
        return half_pow * half_pow * x
    
x = 2
n = 9
print(myPow(x,n))