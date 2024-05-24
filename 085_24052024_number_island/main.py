def numIslands(grid: list[list[str]]) -> int:
    if not grid:
        return 0
    
    def dfs(grid, i, j):
        # Base case: if out of bounds or at a cell that is not '1', return
        if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]) or grid[i][j] == '0':
            return
        
        # Mark the cell as visited by setting it to '0'
        grid[i][j] = '0'
        
        # Visit all adjacent cells (up, down, left, right)
        dfs(grid, i + 1, j)
        dfs(grid, i - 1, j)
        dfs(grid, i, j + 1)
        dfs(grid, i, j - 1)
    
    num_islands = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '1':
                dfs(grid, i, j)  # Start DFS to mark all connected '1's
                num_islands += 1  # Increment island count
    
    return num_islands


grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]

print(numIslands(grid))