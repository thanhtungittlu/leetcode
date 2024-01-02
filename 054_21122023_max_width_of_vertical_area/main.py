def maxWidthOfVerticalArea(points):
    """
    :type points: List[List[int]]
    :rtype: int
    """
    list_x = []
    for point in points:
        list_x.append(point[0])
    list_x.sort()
    rel = 0
    for i in range(1, len(list_x)-1):
        rel = max(rel, list_x[i] - list_x[i-1])
    return rel



points = [[8,7],[9,9],[7,4],[9,7]]
print(maxWidthOfVerticalArea(points))