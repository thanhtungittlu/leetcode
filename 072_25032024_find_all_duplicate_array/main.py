def findDuplicates(nums: list) -> list:
    check_set = set()
    ans = []
    for num in nums:
        if num not in check_set:
            check_set.add(num)
        else:
            ans.append(num)
    return ans


nums = [4, 3, 2, 7, 8, 2, 3, 1]
print(findDuplicates(nums))
