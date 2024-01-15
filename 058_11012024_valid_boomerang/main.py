def isBoomerang(points):
    """
    :type points: List[List[int]]
    :rtype: bool
    """
    if points[2][0] - points[0][0] == 0:
        if points[1][0] == points[2][0]:
            return False
        return True
    m = (points[2][1] - points[0][1]) / (points[2][0] - points[0][0])
    print("tu so: ", points[2][1] - points[0][1])
    print("mau so: ", points[2][0] - points[0][0])
    print("He so goc: ",m)
    if points[1][1] - points[0][1] == m *(points[1][0] - points[0][1]):
        return False
    return True

           
points = [[0,0],[2,1],[2,1]]
print(isBoomerang(points))