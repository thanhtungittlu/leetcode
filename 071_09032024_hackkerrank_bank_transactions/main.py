
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
    balance = 0
    max_transactions = 0
    transactions.sort(reverse=True)

    for t in transactions:
        if balance + t >= 0:
            balance += t
            max_transactions += 1

    return max_transactions


transaction = [1, 2, 3, 4, -10, -1, -2, -3, -4, 5]
print(maximum_number_of_transactions_possible(transaction))
