from collections import defaultdict


def beautifulSubsets(nums: list[int], k: int) -> int:
    nums = sorted(nums)
    n = len(nums)
    check = defaultdict(int)
    def backtrack(current):
        if current == n:
            return 0

        take = 0
        if not nums[current] - k in check:
            check[nums[current]] += 1
            take = 1 + backtrack(current + 1)
            check[nums[current]] -= 1
            if check[nums[current]] == 0:
                check.pop(nums[current])

        notTake = backtrack(current + 1)
        return take + notTake

    return backtrack(0)
if __name__ == "__main__":
    nums = [2,4,6]
    k = 2
    print(beautifulSubsets(nums, k))