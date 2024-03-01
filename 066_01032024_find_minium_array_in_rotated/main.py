def findMin(nums: list) -> int:
    is_check = nums[0]
    while nums[-1] - is_check < 0:
        is_check = nums.pop(-1)
    return is_check

nums = [11,13,15,17]
print(findMin(nums))