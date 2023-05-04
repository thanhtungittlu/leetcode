# def containsDuplicate(nums):
#     """
#     :type nums: List[int]
#     :rtype: bool
#     """
#     dict_nums = {}
#     for ele in nums:
#         if ele not in dict_nums:
#             dict_nums[ele] = 1
#         else:
#             return True
#     return False

def containsDuplicate(nums):
    """
    :type nums: List[int]
    :rtype: bool
    """
    return len(nums) != len(set(nums))


containsDuplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2])
