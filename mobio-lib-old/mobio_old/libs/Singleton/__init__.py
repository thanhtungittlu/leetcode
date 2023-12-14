

class Singleton(object):
    """Singleton decorator."""

    def __init__(self, cls):
        self.__dict__['cls'] = cls

    instances = {}

    def __call__(self):
        if self.cls not in self.instances:
            self.instances[self.cls] = self.cls()
        return self.instances[self.cls]

    def __getattr__(self, attr):
        return getattr(self.__dict__['cls'], attr)

    def __setattr__(self, attr, value):
        return setattr(self.__dict__['cls'], attr, value)


# ------------------Test------------------------
if __name__ == '__main__':
    @Singleton
    class Bar(object):
        def __init__(self):
            self.val = None


    @Singleton
    class Poo(object):
        def __init__(self):
            self.val = None

        def activated(self, acc_id):
            self.val = acc_id


    x = Bar()
    x.val = 'sausage'
    print(x, x.val)
    y = Bar()
    y.val = 'eggs'
    print(y, y.val)
    z = Bar()
    z.val = 'spam'
    print(z, z.val)
    print(x is y is z)

    x = Poo()
    x.val = 'sausage'
    print(x, x.val)
    y = Poo()
    y.val = 'eggs'
    print(y, y.val)

    x = Poo()
    x.activated(123)
    print(x.val)
