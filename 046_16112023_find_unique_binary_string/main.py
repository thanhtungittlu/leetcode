def findDifferentBinaryString(nums):
    """
    :type nums: List[str]
    :rtype: str
    """
    len_nums = len(nums)
    binary_max = "1" * len_nums
    int_max = int(binary_max,2) + 1
    int_array = []
    for num in nums:
        int_array.append(int(num,2))
    for i in range(int_max):
        if i not in int_array:
            binary_string = '{:0{}b}'.format(i, len_nums)
            return binary_string
        
def findDifferentBinaryString(nums): #Cách 2
    ans = []
    for i, n in enumerate(nums):
        if n[i] == '1':
            ans.append('0')
        else:
            ans.append('1')
    return "".join(ans)

nums = ["000","011","001"] #return 11 or 00
print(findDifferentBinaryString(nums))