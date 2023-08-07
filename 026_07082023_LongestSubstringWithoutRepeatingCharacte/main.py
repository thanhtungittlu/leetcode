def lengthOfLongestSubstring(s):
    """
    :type s: str
    :rtype: int
    """
    left = 0 #Vị trí trượt đầu tiên
    max_length = 0 #Độ dài mảng con dài nhất, không trùng ký tự
    char_index = {} #Dict index các ký tự
    for right in range(len(s)):
        #Nếu phần tử đã tổn tại thì tìm lại giá trị left
        if s[right] in char_index and char_index[s[right]] >= left:
            left = char_index[s[right]] + 1 
        char_index[s[right]] = right
        max_length = max(max_length, right-left+1)

    return max_length



list1 = "dvdf"

print(lengthOfLongestSubstring(list1))