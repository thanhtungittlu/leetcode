def removeDuplicates(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    setNums = set()
    uniqueNums = []
    for num in nums:
        if num not in setNums:
            setNums.add(num)
            uniqueNums.append(num)
    nums[:] = uniqueNums 
    return len(nums)   

nums = [-1,0,0,0,0,3,3]
removeDuplicates(nums)
print(nums)

