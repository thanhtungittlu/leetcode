
def maximum_number_of_transactions_possible(transaction):
    res = 0
    cur_sum = 0
    for tran in transaction:
        if cur_sum + tran >= 0:
            cur_sum += tran
            res += 1   
    return res


transaction = [-1, -2, 3, -3, 0]
print(maximum_number_of_transactions_possible(transaction))