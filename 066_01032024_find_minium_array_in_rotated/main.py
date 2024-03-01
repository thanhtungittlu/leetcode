# def findMin(nums: list) -> int:
#     is_check = nums[0]
#     while nums[-1] - is_check < 0:
#         is_check = nums.pop(-1)
#     return is_check




def findMin(nums: list) -> int:
    low, high = 0, len(nums) - 1
    
    while low < high:
        mid = (low + high) // 2
        
        # Nếu phần tử ở giữa lớn hơn phần tử cuối cùng, chúng ta ở bên phải của điểm xoay
        if nums[mid] > nums[high]:
            low = mid + 1
        # Nếu phần tử ở giữa nhỏ hơn phần tử cuối cùng, chúng ta ở bên trái của điểm xoay
        elif nums[mid] < nums[high]:
            high = mid
        # Nếu có sự trùng khớp, giảm high vì chúng ta đã kiểm tra mid
        else:
            high -= 1
    
    return nums[low]

# Example usage:
nums = [4, 5, 6, 7, 0, 1, 2]
result = findMin(nums)
print(result)