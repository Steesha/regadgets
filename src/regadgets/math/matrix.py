def matrix_multiply(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])
    
    if cols_A != rows_B:
        raise ValueError("矩阵 A 的列数必须等于矩阵 B 的行数")
    
    C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A): 
                C[i][j] += A[i][k] * B[k][j]
    
    return C

def matrix_inverse(A):
    n = len(A) 
    
    I = [[float(i == j) for i in range(n)] for j in range(n)]
    
    for i in range(n):
        A[i] = A[i] + I[i]
    
    for i in range(n):
        if A[i][i] == 0:
            for j in range(i+1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
            else:
                raise ValueError("矩阵不可逆")
        
        divisor = A[i][i]
        for j in range(2 * n):
            A[i][j] /= divisor
        
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(2 * n):
                    A[j][k] -= factor * A[i][k]
    
    inverse = [row[n:] for row in A]
    
    return inverse

def matrix_determinant(A):
    n = len(A)
    
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    
    det = 0
    for c in range(n):
        sub_matrix = [[A[i][j] for j in range(n) if j != c] for i in range(1, n)]
        det += ((-1) ** c) * A[0][c] * matrix_determinant(sub_matrix)
    
    return det

def generate_matrix_square(data, n):
    result = []
    if len(data) != n*n:
        return []
    for i in range(0, n*n, n):
        r = []
        for j in range(n):
            r.append(data[j + i])
        result.append(r)
    return result

def flat_matrix(matrix):
    data = []
    for i in matrix:
        for j in i:
            data.append(j)
    return data