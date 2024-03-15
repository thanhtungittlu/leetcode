def minimumBribes(q):
    first_q = sorted(q)
    list_bribes = []
    for i in range(len(q)):
        list_bribes.append(q[i] - first_q[i])
    res = 0   
    for bribes in list_bribes:
        if bribes < 0:
            continue
        elif bribes >= 3:
            return print("Too chaotic")
        else:
            res += bribes
    return print(res)


q = [1, 2, 5, 3, 7, 8, 6, 4]
print(minimumBribes(q))