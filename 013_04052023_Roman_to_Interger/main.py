def romanToInt(s):
    """
    :type s: str
    :rtype: int
    """
    roman_dict = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000
    }
    result = 0
    prev_val = 0
    for i in range(len(s) - 1, -1, -1):
        curr_val = roman_dict[s[i]]
        if curr_val < prev_val:
            result -= curr_val
        else:
            result += curr_val
        prev_val = curr_val
    return result
