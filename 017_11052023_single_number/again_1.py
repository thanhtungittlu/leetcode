def singleNumber(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    dictS = {}
    for num in nums:
        if num in dictS:
            dictS[num] += 1
        else:
            dictS[num] = 1
    
    for key, value in dictS.items():
        if value == 1:
            return key


nums = [4]      
print(singleNumber(nums))
