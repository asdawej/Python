from matrix import *


def zeros(*args: int) -> Matrix:
    '''
    Create a Matrix with 0\n
    ---
    zeros(2, 3) ->\n
    [[0, 0, 0],\n
    [0, 0, 0]]\n
    zeros(2) ->\n
    [[0, 0],\n
    [0, 0]]
    '''
    temp: list[list] = []
    if len(args) == 1:
        for i in range(args[0]):
            temp.append([])
            for _ in range(args[0]):
                temp[-1].append(0)
        return Matrix(temp)
    else:
        for i in range(args[0]):
            temp.append([])
            for _ in range(args[1]):
                temp[-1].append(0)
        return Matrix(temp)


def ones(*args: int) -> Matrix:
    '''
    Create a Matrix with 1\n
    ---
    ones(2, 3) ->\n
    [[1, 1, 1],\n
    [1, 1, 1]]\n
    ones(2) ->\n
    [[1, 1],\n
    [1, 1]]
    '''
    if len(args) == 1:
        temp = zeros(args[0])
    else:
        temp = zeros(args[0], args[1])
    temp[...] = 1
    return temp


def eye(*args: int) -> Matrix:
    '''
    Create a Matrix with only the diagnal being 1\n
    ---
    eye(2, 3) ->\n
    [[1, 0, 0],\n
    [0, 1, 0]]\n
    eye(2) ->\n
    [[1, 0],\n
    [0, 1]]
    '''
    if len(args) == 1:
        temp = zeros(args[0])
    else:
        temp = zeros(args[0], args[1])
    for i in range(1, min(temp.shape.m, temp.shape.n)+1):
        temp[i, i] = 1
    return temp


class Element_Matrix_Arg(object):
    '''Embedded class, may not use it'''

    def __init__(self, i: int, j: int, k: int) -> NoReturn:
        self.i = i
        self.j = j
        self.k = k

    def __eq__(self, other: 'Element_Matrix_Arg') -> bool:
        return self.i == other.i and self.j == other.j and self.k == other.k


class Element_Matrix(Matrix):
    '''
    Members are /mat/, /shape.m/, /shape.n/, /arg.i/, /arg.j/, /arg.k/\n
    Methods are /T/, /enblock/, /unblock/
    '''

    def __init__(self, n: int, i: int, j: int = None, *, k: int = None) -> NoReturn:
        '''
        To create an Elementary Matrix, you should give n, i,
        and must give j or k at least one arg\n
        - If i and j, a swap-Matrix for row_i and row_j
        - If i and k, a mul-Matrix for k times row_i
        - If i, j and k, a muladd-Matrix for k times row_i add to row_j
        ---
        Members are /mat/, /shape.m/, /shape.n/, /arg.i/, /arg.j/, /arg.k/
        '''
        temp_pre = eye(n)
        if j:
            if k:
                temp_pre[j, i] = k
            else:
                temp_pre[i, i] = 0
                temp_pre[j, j] = 0
                temp_pre[i, j] = 1
                temp_pre[j, i] = 1
        elif k:
            temp_pre[i, i] = k
        else:
            raise TypeError('Arguments missing for j or k')
        self.mat = temp_pre.mat
        self.shape = Shape(n, n)
        self.arg = Element_Matrix_Arg(i, j, k)


def gauss(mat: Matrix, record: bool = False) -> Matrix | tuple[Matrix, list[Element_Matrix]]:
    '''
    Gauss Simplification, or the partial rref\n
    ---
    gauss()
    '''
    pass


def ifgauss(mat: Matrix) -> bool:
    '''
    To check whether the Matrix is Gauss-Simplified
    '''
    pass


def jordan(mat: Matrix, record: bool = False) -> Matrix | tuple[Matrix, list[Element_Matrix]]:
    '''
    Add to Gauss Simplification, the second part of Gauss-Jordan Simplification, or rref\n
    ---
    jordan()
    '''
    pass


def rref(mat: Matrix, record: bool = False) -> Matrix | tuple[Matrix, list[Element_Matrix]]:
    '''
    Gauss-Jordan Simplification\n
    ---
    rref()
    '''
    pass


def ifrref(mat: Matrix) -> bool:
    '''
    To check whether the Matrix is rrefed
    '''
    pass


if __name__ == '__main__':
    print('zeros & ones & eye test:')
    print(zeros(3), '\n')
    print(ones(2, 3), '\n')
    print(eye(3), '\n')

    print('Element_Matrix test:')
    print(Element_Matrix(4, 1, 4), '\n')
    print(Element_Matrix(4, 1, k=5), '\n')
    print(Element_Matrix(4, 1, 3, k=5), '\n')
