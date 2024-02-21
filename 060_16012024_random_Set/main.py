import random
class RandomizedSet(object):
    def __init__(self):
        self.list_ele = []
        self.index_ele = {}
        self.len = 0
    def insert(self, val):
        """
        :type val: int
        :rtype: bool
        """
        if val in self.index_ele:
            return False
        self.list_ele.append(val)
        self.len += 1
        self.index_ele[val] = self.len -1 
        return True

    def remove(self, val):
        """
        :type val: int
        :rtype: bool
        """
        if val not in self.index_ele:
            return False
        index_val = self.index_ele[val]
        self.index_ele[self.list_ele[self.len-1]] = index_val #Đổi phần tử cuối cùng trong dict lên phần tử đã bị xóa
        self.list_ele.remove(val)
        self.index_ele.pop(val)
        self.len -= 1
        return True
    def getRandom(self):
        """
        :rtype: int
        """
        return random.choice(self.list_ele)


# Your RandomizedSet object will be instantiated and called as such:
obj = RandomizedSet()
val = 3
obj.insert(1)
obj.insert(5)
obj.insert(val)
obj.insert(4)
obj.insert(2)
obj.remove(val)
# param_2 = obj.remove(val)
param_3 = obj.getRandom()
print(param_3)