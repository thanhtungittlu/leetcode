# from heapq import heappush, heappop


# def firstMissingPositive(nums: list) -> int:  # time limited
#     hq = []
#     for num in nums:
#         if num > 0 and num not in hq:
#             heappush(hq, num)
#     res = 0
#     while hq:
#         min_el = heappop(hq)
#         if min_el - res == 1:
#             res = min_el
#         else:
#             res += 1
#             break
#     else:
#         res += 1
#     return res

# Tư tưởng là phần tử  nếu có sẽ nằm trong khoảng từ 0->n
def firstMissingPositive(nums: list) -> int:
    for i in range(len(nums)):
        current = nums[i]
        while current - 1 < len(nums) and current - 1 >= 0:
            next = nums[current - 1]
            nums[current - 1] = float('-inf')
            current = next

    for i in range(len(nums)):
        if nums[i] != float('-inf'):
            return i + 1

    return len(nums) + 1


nums = [3, 4, -1, 1]
print(firstMissingPositive(nums))
