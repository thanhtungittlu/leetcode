from heapq import heappush, heappop


def maximum_number_of_transactions_possible(transactions):
    _sum, ans, hq = 0, 0, []
    for transaction in transactions:
        ans += 1
        _sum += transaction
        if transaction < 0:
            heappush(hq, transaction)
        while _sum < 0 and hq:
            min_el = heappop(hq)
            _sum -= min_el
            ans -= 1
    return ans


transaction = [1, 2, 3, 4, -10, -11, -12, -3, 5]
print(maximum_number_of_transactions_possible(transaction))
