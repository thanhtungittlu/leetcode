import heapq

def findKthLargest(nums, k):
    """
    :type nums: List[int]
    :type k: int
    :rtype: int
    """
    x=heapq.nlargest(k,nums)
    # In ra danh sách mới sắp xếp từ lớn về nhỏ của nums, và có k phần tử
    print("x: ", x)
    return x[k-1]
    
    

nums = [2,-1,3,9,4,3,2,1] 
k = 4
print(findKthLargest(nums, k))