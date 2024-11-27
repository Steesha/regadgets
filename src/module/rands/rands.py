from ctypes import c_int, c_uint
from typing import List

class GLIBCRand():
    def __init__(self, seed: int):
        '''
        /* We must make sure the seed is not 0.  Take arbitrarily 1 in this case.  */
        if (seed == 0)
        seed = 1;
        '''
        if seed == 0:
            seed = 1
        self.r = [0 for _ in range(34)]
        self.r[0] = c_int(seed).value
        for i in range(1, 31):
            self.r[i] = (16807 * self.r[i - 1]) % 2147483647
        for i in range(31, 34):
            self.r[i] = self.r[i - 31]
        self.k = 0
        for _ in range(34, 344):
            self.rand()
    
    def rand(self) -> int:
        self.r[self.k] = self.r[(self.k - 31) % 34] + self.r[(self.k - 3) % 34]
        r = c_uint(self.r[self.k]).value >> 1
        self.k = (self.k + 1) % 34
        return r

    def rands(self, count: int) -> List[int]:
        return [self.rand() for _ in range(count)]

class WindowsRand():
    def __init__(self, seed: int):
        self.holdrand = seed
    
    def rand(self) -> int:
        self.holdrand = self.holdrand * 214013 + 2531011
        return (self.holdrand >> 16) & 0x7fff
    
    def rands(self, count: int) -> List[int]:
        return [self.rand() for _ in range(count)]