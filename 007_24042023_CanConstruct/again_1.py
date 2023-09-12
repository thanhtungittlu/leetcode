def canConstruct(ransomNote, magazine):
    """
        :type ransomNote: str
        :type magazine: str
        :rtype: bool
    """
    for char in ransomNote:
        if char not in magazine:
            return False
        else:
            magazine = magazine.replace(char,"",1)

    return True



ransomNote = "aab"
magazine = "aa"
print(canConstruct(ransomNote, magazine))