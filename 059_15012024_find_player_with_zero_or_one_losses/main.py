def findWinners(matches):
    """
    :type matches: List[List[int]]
    :rtype: List[List[int]]
    """
    result_match = {}
    for match in matches:
        if match[0] not in result_match:
            result_match[match[0]] = {
                "win": 1,
                "lose": 0
            }
        else:
            result_match[match[0]]["win"] += 1
        
        if match[1] not in result_match:
            result_match[match[1]] = {
                "win": 0,
                "lose": 1
            }
        else:
            result_match[match[1]]["lose"] += 1
    have_not_lost = []
    have_one_lost = []
    for key, value in result_match.items():
        if value["lose"] == 0:
            have_not_lost.append(key)
        elif value["lose"] == 1:
            have_one_lost.append(key)
    
    have_not_lost.sort()
    have_one_lost.sort()
    return [have_not_lost,have_one_lost]


matches = [[1,3],[2,3],[3,6],[5,6],[5,7],[4,5],[4,8],[4,9],[10,4],[10,9]] #output: [[1,2,10],[4,5,7,8]]
print(findWinners(matches))