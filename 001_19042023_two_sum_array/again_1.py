def twoSum(nums, target):
    if len(nums) == 2:
        return [0,1]
    
    for i in range(len(nums)-1):
        check = target - nums[i]
        if check in nums:
            indexCheck = nums.index(check)
            if indexCheck != i and nums.count(check) == 1:
                return [i, indexCheck]
            elif nums.count(check) > 1:
                nums.remove(nums[i])
                return [i, nums.index(check)+1]

nums = [3,2,3]
target = 6
print(twoSum(nums, target))