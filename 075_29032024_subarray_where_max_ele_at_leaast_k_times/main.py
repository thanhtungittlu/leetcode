def countSubarrays(nums: list, k: int) -> int:
    max_element = max(nums)
    count, left, result = 0, 0, 0
    n = len(nums)

    for right, num in enumerate(nums):
        if num == max_element:
            count += 1

        while count >= k:
            result += (n - right)
            if nums[left] == max_element:
                count -= 1
            left += 1
    return result


nums = [1, 3, 2, 3, 3, 2, 2, 3, 1]
k = 2
print(countSubarrays(nums, k))
