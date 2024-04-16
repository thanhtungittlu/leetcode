def removeKdigits(num: str, k: int) -> str:
    hold_left = 0
    hold_char_first = ""
    while k > 0:
        len_cur_num = len(num)
        hold_right = len_cur_num - k - 1
        num_check = num[hold_left:(len_cur_num - hold_right)]
        min_num_check = min(list(num_check))
        index_min = num.find(min_num_check)
        if hold_left - 1 >= 0:
            hold_char_first = num[hold_left - 1]
        num = hold_char_first + num[index_min:]
        k = k - index_min + hold_left
        hold_left += 1

    return num


num = "84137292024814"  # 137292024814 =>  #1292024814 =>  #122024814
k = 5
print(removeKdigits(num, k))
