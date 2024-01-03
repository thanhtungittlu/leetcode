def numberOfBeams(bank):
    """
    :type bank: List[str]
    :rtype: int
    """
    res = 0
    row_cur = 0
    
    while row_cur < len(bank):
        row_bottom = row_cur + 1
        if row_bottom >= len(bank):
            break
        number_cam_cur = bank[row_cur].count("1")
        number_cam_bottom = bank[row_bottom].count("1")
        while number_cam_bottom == 0:
            row_bottom +=1
            if row_bottom >= len(bank):
                break
            number_cam_bottom = bank[row_bottom].count("1")
        res += number_cam_cur * number_cam_bottom
        row_cur = row_bottom

    return res

def numberOfBeams(bank):
    prev, ans = 0, 0
    for i in bank:
        current = i.count('1')
        if current:
            ans += prev * current
            prev = current
    return ans



bank = ["011001","000000","010100","001000"]
bank2 = ["000","111","000"]
print(numberOfBeams(bank))
