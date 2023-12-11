def findSpecialInteger(arr):
        """
        :type arr: List[int]
        :rtype: int
        """
        dict_arr= {}
        len_arr_check = len(arr) / 4
        for elm in arr:
            if elm in dict_arr:
                dict_arr[elm] += 1
            else:
                dict_arr[elm] = 1
        
        for key, value in dict_arr.items():
            if value > len_arr_check:
                return key
            
