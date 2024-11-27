class Symbol:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name
    def __rshift__(self, other):
        if isinstance(other, Symbol):
            expression =  Symbol(f"({self.name} >> {other.name})")
        else:
            expression =  Symbol(f"({self.name} >> {other})")
        return expression
    def __lshift__(self, other):
        if isinstance(other, Symbol):
            expression = Symbol(f"({self.name} << {other.name})")
        else:
            expression =  Symbol(f"({self.name} << {other})")
        return expression
    def __rxor__(self, other):
        if isinstance(other, Symbol):
            expression =  Symbol(f"({self.name} ^ {other.name})")
        else:
            expression =  Symbol(f"({self.name} ^ {other})")
        return expression
    def __xor__(self, other):
        if isinstance(other, Symbol):
            expression = Symbol(f"({self.name} ^ {other.name})")
        else:
            expression =  Symbol(f"({self.name} ^ {other})")
        return expression
    def __add__(self, other):
        if isinstance(other, Symbol):
            expression = Symbol(f"({self.name} + {other.name})")
        else:
            expression = Symbol(f"({self.name} + {other})")
        return expression
    def __and__(self, other):
        if isinstance(other, Symbol):
            expression =  Symbol(f"({self.name} & {other.name})")
        else:
            expression = Symbol(f"({self.name} & {other})")
        return expression

class AList:
    def __init__(self, nums):
        self.nums = [Symbol(str(num)) for num in nums]
    def __getitem__(self, key):
        return self.nums[key]
    def copy(self):
        return AList(self.nums)
    def __len__(self):
        return len(self.nums)
    def __setitem__(self, key, value):
        print(f"new_{self.nums[key]} = {value}")
        self.nums[key] = Symbol(f"new_{self.nums[key].name}")
    def __eq__(self, other):
        print(f"{self.nums} == {other}")
        return self.nums == other