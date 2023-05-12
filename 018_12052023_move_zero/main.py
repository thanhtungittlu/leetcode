# def moveZeroes(nums):
#     """
#     :type nums: List[int]
#     :rtype: None Do not return anything, modify nums in-place instead.
#     """
#     result = []
#     i = 0
#     dem = 0
#     while i < len(nums):
#         if nums[i] != 0:
#             result.append(nums[i])
#         else:
#             dem += 1
#         i += 1
#     for d in range(dem):
#         result.append(0)

#     return result


def moveZeroes(nums):
    i = 0
    for j in range(len(nums)):
        if nums[j] != 0:
            nums[i] = nums[j]
            i += 1

   
    nums[i:] = [0] * (len(nums) - i)

    return nums


print(moveZeroes([0, 0, 0, 1, 0, 3]))
