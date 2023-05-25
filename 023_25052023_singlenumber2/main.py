def singleNumber(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    dictN = {
        nums[0]: 1
    }
    for i in nums[1:]:
        if i in dictN:
            dictN[i] += 1
        else:
            dictN[i] = 1
    for k, v in dictN.items():
        if v == 1:
            return k
