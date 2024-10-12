import math
from typing import List

def dct_transform(values: List[float]) -> List[float]:
    n = len(values)
    result = [0.0] * n
    factor = math.sqrt(2.0 / n)
    
    for i in range(n):
        sum_val = 0.0
        for j in range(n):
            sum_val += values[j] * math.cos((j + 0.5) * i * math.pi / n)
        coeff = factor if i > 0 else math.sqrt(1.0 / n)
        result[i] = round(coeff * sum_val)
    
    return result

def idct_transform(values: List[float]) -> List[float]:
    n = len(values)
    result = [0.0] * n
    factor = math.sqrt(2.0 / n)
    
    for i in range(n):
        sum_val = 0.0
        for j in range(n):
            coeff = factor if j > 0 else math.sqrt(1.0 / n)
            sum_val += coeff * values[j] * math.cos((i + 0.5) * j * math.pi / n)
        result[i] = round(sum_val)
    return result