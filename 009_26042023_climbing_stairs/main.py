# def climbStairs(n):
#     if n == 1:
#         return 1
#     elif n == 2:
#         return 2
#     else:
#         return climbStairs(n-1) + climbStairs(n-2)
def climbStairs(n):
    """
    :type n: int
    :rtype: int
    """
    if n == 1:
        return 1
    if n == 2:
        return 2
    else:
        dp = [0] * (n+1)
        dp[1] = 1
        dp[2] = 2
        for i in range(3, n+1):
            dp[i] = dp[i-1] + dp[i-2]
        return dp[n]
