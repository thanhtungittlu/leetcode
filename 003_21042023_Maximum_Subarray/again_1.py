def maxSubArray(nums):
    current_sum = 0
    max_sum = nums[0]
    for num in nums:
        if current_sum < 0:
            current_sum = 0
        current_sum += num
        if current_sum > max_sum:
            max_sum = current_sum

    return max_sum
nums = [-2,-1,-3,-4,-1,-2,-1,-5,-4]
print(maxSubArray(nums))