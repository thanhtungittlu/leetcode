import random
class RandomizedSet(object):
    def __init__(self):
        self.list_ele = []
        
    def insert(self, val):
        """
        :type val: int
        :rtype: bool
        """
        if val not in self.list_ele:
            self.list_ele.append(val)
            return True
        else:
            return False
        

    def remove(self, val):
        """
        :type val: int
        :rtype: bool
        """
        if val in self.list_ele:
            self.list_ele.remove(val)
            return True
        else:
            return False
        

    def getRandom(self):
        """
        :rtype: int
        """
        return random.choice(self.list_ele)


# Your RandomizedSet object will be instantiated and called as such:
obj = RandomizedSet()
val = 3
param_1 = obj.insert(val)

# param_2 = obj.remove(val)
param_3 = obj.getRandom()
print(param_3)