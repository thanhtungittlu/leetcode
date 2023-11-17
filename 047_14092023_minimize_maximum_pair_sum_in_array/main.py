def minPairSum(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    new_nums = sorted(nums)
    start = 0
    end = len(nums) - 1
    result = 0
    while end > start:
        result = max(new_nums[start] + new_nums[end], result)
        end -=1
        start +=1
    return result
    



# nums1 = [2,3,3,5]
# print(minPairSum(nums1)) #output 7

# nums1 = [2,3,5,5]
# print(minPairSum(nums1)) #output 8

# nums2 = [2,3,4,4,5,6]
# print(minPairSum(nums2)) #output 8

# nums3 = [1,3,3,3,5,5,22,23] #output 25
# print(minPairSum(nums3))

nums4 = [4,1,5,1,2,5,1,5,5,4]  #output 8
print(minPairSum(nums4))
