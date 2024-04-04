def exist(board: list, word: str) -> bool:
    m = len(board)
    n = len(board[0])
    visited = set()

    def dfs(i, j, word_idx):
        if word_idx == len(word):
            return True
        if i < 0 or j < 0 or i >= m or j >= n:
            return False
        if word[word_idx] != board[i][j]:
            return False
        if (i, j) in visited:
            return False

        visited.add((i, j))
        result = dfs(i + 1, j, word_idx + 1) or \
            dfs(i - 1, j, word_idx + 1) or \
            dfs(i, j + 1, word_idx + 1) or \
            dfs(i, j - 1, word_idx + 1)

        visited.remove((i, j))
        return result

    for i in range(m):
        for j in range(n):
            if dfs(i, j, 0):
                return True
    return False


board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
word = "ABCCED"
print(exist(board, word))
