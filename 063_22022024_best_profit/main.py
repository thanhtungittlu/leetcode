def maxProfit(prices):
    """
    :type prices: List[int]
    :rtype: int
    """
    min_price = prices[0]
    max_profit = 0

    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)

    return max_profit

prices = [7,1,5,3,6,4]
print(maxProfit(prices))