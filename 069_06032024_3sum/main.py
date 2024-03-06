# def threeSum(nums: list) -> list:  litmit time
#     res = []
#     list_positive = [num for num in nums if num > 0]
#     len_positive = len(list_positive)
#     sum_positive = sum(list_positive)        
#     list_negative = [num for num in nums if num < 0]
#     len_negative = len(list_negative)
#     sum_negative = sum(list_negative)        
#     count_0 = nums.count(0)
#     for i in range(len_positive-1):
#         for j in range(i+1, len_positive,1):
#             two_sum = list_positive[i] + list_positive[j]
#             expectation = 0 - two_sum
#             if expectation < sum_negative:
#                 continue
#             if expectation in list_negative:
#                 cur_res = sorted([list_positive[i], list_positive[j], expectation])
#                 if cur_res not in res:
#                     res.append(cur_res)

#     for i in range(len_negative-1):
#         for j in range(i+1, len_negative,1):
#             two_sum = list_negative[i] + list_negative[j]
#             expectation = 0 - two_sum
#             if expectation > sum_positive:
#                 continue
#             if expectation in list_positive:
#                 cur_res = sorted([list_negative[i], list_negative[j], expectation])
#                 if cur_res not in res:
#                     res.append(cur_res)
#     if count_0:
#         for negative in list_negative:
#             if -negative in list_positive:
#                 cur_res = [negative, 0, -negative]
#                 if cur_res not in res:
#                     res.append(cur_res)
#     if count_0 >=3:
#         res.append([0,0,0])
#     return res


def threeSum(nums: list) -> list:
    result = []
    nums.sort()

    for i in range(len(nums)-2):
        # Skip duplicates
        if i > 0 and nums[i] == nums[i-1]:
            continue
        
        left, right = i + 1, len(nums) - 1

        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]

            if current_sum == 0:
                result.append([nums[i], nums[left], nums[right]])

                # Skip duplicates
                while left < right and nums[left] == nums[left+1]:
                    left += 1
                while left < right and nums[right] == nums[right-1]:
                    right -= 1

                left += 1
                right -= 1
            elif current_sum < 0:
                left += 1
            else:
                right -= 1

    return result

nums = [-4,-2,1,-5,-4,-4,4,-2,0,4,0,-2,3,1,-5,0]
print(threeSum(nums))