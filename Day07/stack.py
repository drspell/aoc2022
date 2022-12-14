class Stack:
    def __init__(self, lst=None):
        if lst is None:
            self.data = list()
        else:
            self.data = lst.copy()

    def push(self, val):
        self.data = [val] + self.data

    def pop(self):
        if self.empty():
            raise Exception("stack is empty")

        val = self.data[0]
        self.data = self.data[1:]
        return val

    def size(self): return len(self.data)

    def empty(self): return len(self.data) == 0

    def peek(self): return self.data[0] if not self.empty() else None

    def __str__(self):
        return self.data.__str__()

    def __repr__(self):
        return self.data.__str__()