def removeKdigits(num: str, k: int) -> str:
    stack = []
    for digit in num:
        while k > 0 and stack and stack[-1] > digit:
            stack.pop()
            k -= 1
        stack.append(digit)

    # Trường hợp còn dư số k, xóa từ cuối stack
    while k > 0:
        stack.pop()
        k -= 1

    # Loại bỏ các số 0 ở đầu
    result = ''.join(stack).lstrip('0')

    return result if result else '0'


# num = "84137292024814"  # 137292024814 =>  #1292024814 =>  #122024814
# k = 5
# num = "1432219"  # 1432219 =>12219 => 1219
# k = 3
num = "84137292024814"
k = 5
print(removeKdigits(num, k))
