def maxSubArray(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    max_sum = 0
    curr_sum = 0

    for num in nums:
        if curr_sum < 0:
            curr_sum = 0

        curr_sum += num
        if curr_sum > max_sum:
            max_sum = curr_sum

    return max_sum


# Kadane algorithm: Khởi tạo 2 tổng ban đầu, rồi lặp qua các phần tử của mảng. Nếu tổng phần tử đấy mà <0 thì reser curent_sum về 0
maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4])
