# def product_arr(nums):
#     ans = 1
#     for num in nums:
#         ans *= num
#     return ans


# def numSubarrayProductLessThanK(nums: list, k: int) -> int: #time limited
#     if k == 0:
#         return 0
#     res = 0
#     length = 1
#     l_num = len(nums)
#     while length <= l_num:
#         for i in range(0, l_num - length + 1):
#             cur_arr = nums[i: length + i]
#             product = product_arr(cur_arr)
#             if product < k:
#                 res += 1
#         length += 1

#     return res


# def numSubarrayProductLessThanK(nums: list, k: int) -> int:
#     if k == 0:
#         return 0
#     l_nums = len(nums)
#     dp = [1] * l_nums
#     ans = 0
#     for step in range(1, l_nums + 1):
#         for i in range(0, l_nums - step + 1):
#             dp[i] = dp[i] * nums[i + step - 1]
#             if dp[i] < k:
#                 ans += 1
#         dp = dp[0: (l_nums - step + 1)]

#     return ans

def numSubarrayProductLessThanK(nums: list, k: int) -> int:
    if k <= 1:
        return 0
    prod = 1
    result = left = 0
    for right, value in enumerate(nums):
        prod *= value
        while prod >= k:
            prod /= nums[left]
            left += 1
        result += right - left + 1
    return result


nums = [10, 5, 2, 6]
k = 100

print(numSubarrayProductLessThanK(nums, k))
