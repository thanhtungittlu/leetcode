def getCommon(nums1: list, nums2: list) -> int:
    len_nums1, len_nums2 = len(nums1), len(nums2)
    cur_index_min1, cur_index_min2 = 0, 0
    while cur_index_min1 < len_nums1 and cur_index_min2 < len_nums2:
        if nums1[cur_index_min1] == nums2[cur_index_min2]:
            return nums1[cur_index_min1]
        if nums1[cur_index_min1] < nums2[cur_index_min2]:
            cur_index_min1 +=1
        else:
            cur_index_min2 +=1

    return -1

nums1 = [5,6,7]
nums2 = [2,6]

print(getCommon(nums1, nums2))