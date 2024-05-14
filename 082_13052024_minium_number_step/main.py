
def minSteps(s: str, t: str) -> int:
    res = 0
    t_continue = set()
    for c in t:
        if c in t_continue:
            continue

        t_continue.add(c)
        count_c_in_t = t.count(c)
        count_c_in_s = s.count(c)
        if count_c_in_t > count_c_in_s:
            res += count_c_in_t - count_c_in_s
            
    return res

if __name__ == "__main__":
    s = "leetcode" 
    t = "practice"
    print(minSteps(s,t))