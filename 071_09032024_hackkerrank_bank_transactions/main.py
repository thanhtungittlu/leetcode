from heapq import heappush, heappop


# def maximum_number_of_transactions_possible(transaction):
#     res = 0
#     cur_sum = 0
#     list_negative = []
#     for tran in transaction:
#         if tran >= 0:
#             cur_sum += tran
#             res += 1
#         else:
#             list_negative.append(tran)
#     list_negative.sort(reverse=True)
#     for negative in list_negative:
#         if cur_sum + negative >= 0:
#             cur_sum += negative
#             res += 1
#     return res


def maximum_number_of_transactions_possible(transactions):
    """
    Finds the maximum number of transactions possible while maintaining a non-negative balance.

    Args:
        transactions: A list of integers representing transaction amounts.

    Returns:
        The maximum number of transactions possible.
    """

    sum_, ans, pq = 0, 0, []
    for transaction in transactions:
        sum_ += transaction
        ans += 1
        if transaction < 0:
            heappush(pq, transaction)  # Add negative transactions to min-heap

        while sum_ < 0 and pq:  # Remove negative transactions if sum becomes negative
            min_element = heappop(pq)
            sum_ -= min_element
            ans -= 1

    return ans


transaction = [1, 2, 3, 4, -10, -11, -12, -3, 5]
print(maximum_number_of_transactions_possible(transaction))
