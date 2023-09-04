# def generate_subsets(arr, index, subset, subsets):
#     if index == len(arr):
#         subsets.append(subset[:])  # Copy the current subset
#         return

#     # Include the current element in the subset
#     subset.append(arr[index])
#     generate_subsets(arr, index + 1, subset, subsets)

#     # Exclude the current element from the subset
#     subset.pop()
#     generate_subsets(arr, index + 1, subset, subsets)

# def subsets(nums):
#     """
#     :type nums: List[int]
#     :rtype: List[List[int]]
#     """
#     subsets = []
#     generate_subsets(nums, 0, [], subsets)
#     return subsets


def subsets(nums):
    list_subset = [[]]
    for num in nums:
        list_subset_with_num = []
        for subset in list_subset:
            list_subset_with_num.append( subset + [num])
        list_subset.extend(list_subset_with_num)
    return list_subset
array = [1, 2, 3, 4]
print(subsets(array))
