def maxLengthBetweenEqualCharacters(s: str) -> int:
    appearances = {}
    for i, char in enumerate(s):
        if char not in appearances:
            appearances[char] = (i, i)  # initialize with (first, last) as (i, i)
        else:
            appearances[char] = (appearances[char][0], i)  # update the last appearance
    
    max_length = -1
    for first, last in appearances.values():
        if last > first:  # There must be at least two occurrences of the character
            max_length = max(max_length, last - first - 1)

    return max_length


if __name__ == "__main__":
    s = 'cbzxy'
    print(maxLengthBetweenEqualCharacters(s))