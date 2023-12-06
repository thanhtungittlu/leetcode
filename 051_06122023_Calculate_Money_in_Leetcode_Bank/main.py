def totalMoney(n):
    """
    :type n: int
    :rtype: int
    """
    number_week_full = n // 7
    number_day_remain = n % 7
    rel_week = 0
    # for i in range(number_week_full):
    #     rel_week += 28 + (7*i)
    rel_week = 28 * number_week_full + 7 * number_week_full*(number_week_full - 1)//2
    
    money_t2_week = number_week_full + 1
    rel_day_remain = number_day_remain * (money_t2_week + money_t2_week + number_day_remain - 1 ) // 2

    return rel_week + rel_day_remain

n = 26
print(totalMoney(n))