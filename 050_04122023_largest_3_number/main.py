def largestGoodInteger_1(num):
    """
    :type num: str
    :rtype: str
    """
    result = ''
    arr_num = list(num)
    for i in range(len(arr_num) - 2):
        if arr_num[i] == arr_num[i+1] == arr_num[i+2]:
            result =  max(str(arr_num[i]) + str(arr_num[i]) + str(arr_num[i]), result)
            
            
    return result

def largestGoodInteger(num):
    """
    :type num: str
    :rtype: str
    """
    for i in range(9,-1,-1):
        check = str(i) * 3
        if num.find(check) != -1:
            return check  
    return ''            

num = "6777133339"
print(largestGoodInteger(num))
