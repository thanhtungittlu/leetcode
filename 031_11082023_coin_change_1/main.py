def coinChange(coins, amount):
    """
    :type coins: List[int]
    :type amount: int
    :rtype: int
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    # Duyệt qua mỗi giá trị từ 1 đến amount: tính số lượng ít nhất các đồng tiền cần để đạt được từng giá trị nhỏ hơn amount
    for i in range(1, amount + 1):
        # Duyệt qua danh sách coins để cập nhật dp[i]
        for coin in coins:
            if i - coin >= 0:
                dp[i] = min(dp[i], dp[i - coin] + 1) #dp[i-coin] + 1 là số lượng đồng tiền cần để tạo ra số tiền i-coin, cộng với thêm 1 đồng tiền coin
    
    return dp[amount] if dp[amount] != float('inf') else -1

coins = [1,2,3]
amount = 10
print(coinChange(coins, amount))