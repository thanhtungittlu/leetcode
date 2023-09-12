from collections import Counter

def minDeletions(s):
    """
    :type s: str
    :rtype: int
    """
    character_count = Counter(s)
    frequencies = list(character_count.values())
    frequencies.sort(reverse = True)
    return frequencies

s = "ceabaacb"
print(minDeletions(s))
        