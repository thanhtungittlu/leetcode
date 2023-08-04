def combinationSum(candidates, target):
    """
    :type candidates: List[int]
    :type target: int
    :rtype: List[List[int]]
    """
    def backtrack(start, target, path, result):
        if target == 0:
            # Nếu tổng bằng target, thêm path vào kết quả
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if target < candidates[i]:
                # Nếu target nhỏ hơn candidates[i], không thể thêm candidates[i] nữa
                break
            path.append(candidates[i])
            # Gọi đệ quy để tìm các lời giải tiếp theo bằng cách bắt đầu từ vị trí hiện tại
            backtrack(i, target - candidates[i], path, result)
            path.pop()
    
    result = []
    backtrack(0, target, [], result)
    return result