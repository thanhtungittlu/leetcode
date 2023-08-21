def change(amount, coins):
    """
    :type amount: int
    :type coins: List[int]
    :rtype: int
    """
    dp = [0] * (amount+1)
    dp[0] = 1 #Có 1 cách để  taọ ra 0 là 0 sử dụng bất cứ đồng xu nào.
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i-coin]
    
    return dp[amount]

amount = 10
coins = [1,2,5]
print(change(amount, coins))