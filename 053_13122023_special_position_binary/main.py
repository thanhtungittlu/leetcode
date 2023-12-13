def numSpecial(mat):
    """
    :type mat: List[List[int]]
    :rtype: int
    """
    rel = 0
    len_mat = len(mat)
    for i in range(len_mat):
        if sum(mat[i]) != 1:
            continue
        for j in range(len(mat[i])):
            if mat[i][j] == 0:
                continue
            total_col = 0
            for i_count in range(len_mat):
                total_col += mat[i_count][j]
            if total_col != 1:
                continue
            else:
                rel += 1
    return rel

mat = [[1,0,0],[0,1,0],[0,0,1]]
print(numSpecial(mat))