def canJump(nums):
    """
    :type nums: List[int]
    :rtype: bool
    """
    max_reach = 0

    for i in range(len(nums)):
        if i > max_reach:
            return False
        
        max_reach = max(max_reach, i + nums[i]) #Chỉ số tối đa mà có thể nhảy tới

        if max_reach >= len(nums) - 1:
            return True
    
    return False


nums = [3,2,1,0,4]
print(canJump(nums))