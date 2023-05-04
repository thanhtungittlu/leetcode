# def majorityElement(nums):
#     """
#     :type nums: List[int]
#     :rtype: int
#     """
#     nums.sort()
#     return nums[len(nums) // 2]

def majorityElement(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    element_count = {}
    for ele in nums:
        if ele not in element_count:
            element_count[ele] = 1
        else:
            element_count[ele] += 1
    for ele, value in element_count.items():
        if value > len(nums)/2:
            return ele

    print(element_count)


majorityElement([2, 2, 1, 1, 1, 2, 2])
