def findJudge(n, trust):
    """
    :type n: int
    :type trust: List[List[int]]
    :rtype: int
    """
    trust_counts = [0] * (n+1)  #Số  người họ tin tưởng
    trusted_counts = [0] * (n+1) # Số người tin tưởng họ
    # Thẩm phán sẽ k tin ai cả, và số người tin tưởng thẩm phán sẽ là n-1
    for t in trust:
        trust_counts[t[0]] += 1
        trusted_counts[t[1]] += 1
    for i in range(1,n+1):
        if trust_counts[i] == 0 and trusted_counts[i] == n - 1:
            return i
    return -1

n = 3
trust = [[1,2],[2,3]]

print(findJudge(n, trust))
