def _copy_matrix(matrix):
    return [list(row) for row in matrix]


def _validate_matrix(matrix):
    if not matrix or not matrix[0]:
        raise ValueError("matrix must not be empty")
    row_length = len(matrix[0])
    if any(len(row) != row_length for row in matrix):
        raise ValueError("matrix rows must have the same length")


def _validate_square_matrix(matrix):
    _validate_matrix(matrix)
    if len(matrix) != len(matrix[0]):
        raise ValueError("matrix must be square")


def matrix_multiply(A, B):
    _validate_matrix(A)
    _validate_matrix(B)
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
    _validate_square_matrix(A)
    working = _copy_matrix(A)
    n = len(working)

    I = [[float(i == j) for i in range(n)] for j in range(n)]

    for i in range(n):
        working[i] = working[i] + I[i]

    for i in range(n):
        if working[i][i] == 0:
            for j in range(i+1, n):
                if working[j][i] != 0:
                    working[i], working[j] = working[j], working[i]
                    break
            else:
                raise ValueError("矩阵不可逆")

        divisor = working[i][i]
        for j in range(2 * n):
            working[i][j] /= divisor

        for j in range(n):
            if j != i:
                factor = working[j][i]
                for k in range(2 * n):
                    working[j][k] -= factor * working[i][k]

    inverse = [row[n:] for row in working]

    return inverse

def matrix_determinant(A):
    _validate_square_matrix(A)
    n = len(A)

    if n == 1:
        return A[0][0]
    if n == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]

    det = 0
    for c in range(n):
        sub_matrix = [[A[i][j] for j in range(n) if j != c] for i in range(1, n)]
        det += ((-1) ** c) * A[0][c] * matrix_determinant(sub_matrix)

    return det

def generate_matrix_square(data, n):
    if n <= 0:
        raise ValueError("n must be positive")
    if len(data) != n * n:
        raise ValueError("data length must equal n * n")
    return [list(data[i:i + n]) for i in range(0, n * n, n)]

def flat_matrix(matrix):
    _validate_matrix(matrix)
    return [item for row in matrix for item in row]
