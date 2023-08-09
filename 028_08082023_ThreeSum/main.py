def threeSum(nums):
    """
    :type nums: List[int]
    :rtype: List[List[int]]
    """
    nums.sort()
    res = []
    lengthNums = len(nums)

    for i in range(lengthNums - 2):
        if i > 0 and nums[i] == nums[i-1]:
            continue

        left = i+1
        right = lengthNums-1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                res.append([nums[i],nums[left],nums[right]])
                #Tiếp tục tăng left hoặc giảm right để tìm tiếp
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
            if total < 0:
                left += 1
            else:
                right -= 1 
    return res

nums = [-1,0,1,2,-1,-4]
print(threeSum(nums))