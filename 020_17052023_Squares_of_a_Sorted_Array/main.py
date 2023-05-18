# def sortedSquares(nums):
#     """
#     :type nums: List[int]
#     :rtype: List[int]
#     """
#     return sorted(list(map(lambda x: x ** 2, nums)))

def sortedSquares(nums):
    """
    :type nums: List[int]
    :rtype: List[int]
    """
    return sorted([i*i for i in nums])
