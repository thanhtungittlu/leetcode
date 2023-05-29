def singleNumber(nums):
    """
    :type nums: List[int]
    :rtype: List[int]
    """
    dictA = {
        nums[0]: 1
    }
    for num in nums[1:]:
        if num in dictA:
            dictA[num] += 1
        else:
            dictA[num] = 1
    result = []
    for k, v in dictA.items():
        if v == 1:
            result.append(k)
        else:
            continue

    return result
