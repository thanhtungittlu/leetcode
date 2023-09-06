def maxArea(height):
    """
    :type height: List[int]
    :rtype: int
    """
    max_area = 0
    left = 0
    right = len(height) - 1
    while left < right:
        h_left = height[left]
        h_right = height[right]
        curr_area = (right - left) * min(h_left, h_right)
        max_area = max(max_area, curr_area)
        if h_left < h_right:
            left += 1
        else:
            right -= 1

    return max_area

height = [1,8,6,2,5,4,8,3,7]
print(maxArea(height))