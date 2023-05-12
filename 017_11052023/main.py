def singleNumber(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    dict = {
        nums[0]: 1
    }
    for num in nums[1:]:
        if num in dict:
            dict[num] += 1
        else:
            dict[num] = 1
    for k, v in dict.items():
        if v == 1:
            return k


singleNumber([1, 2, 2, 1, 4])


# def singleNumber(nums):
#     xor = 0
#     for num in nums:
#         xor ^= num
#     return xor
