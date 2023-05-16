# def missingNumber(nums):
#     """
#     :type nums: List[int]
#     :rtype: int
#     """
#     sum1 = 0
#     for i in range(len(nums)+1):
#         sum1 += i
#     return sum1 - sum(nums)


# missingNumber([3, 0, 1])


def missingNumber(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    n = len(nums)
    sum1 = (n * (n + 1)) // 2
    return sum1 - sum(nums)
