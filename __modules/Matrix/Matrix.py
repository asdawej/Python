from typing import Any, NoReturn, Iterator
from types import EllipsisType

__author__ = 'asdawej'


class Shape(object):
    '''Embedded class, may not use it'''

    def __init__(self, m: int, n: int) -> NoReturn:
        self.m = m
        self.n = n

    def __eq__(self, other: 'Shape') -> bool:
        return self.m == other.m and self.n == other.n


class Matrix(object):
    '''
    Members are /mat/, /shape.m/, and /shape.n/\n
    Methods are /element/, /row/, /column/
    '''

    def __init__(self, mat: list[list]) -> NoReturn:
        '''
        Automatically, we will count the shape\n
        Members are /mat/, /shape.m/, and /shape.n/
        '''
        s = len(mat[0])
        for x in mat:
            if len(x) != s:
                raise ValueError
        self.mat = mat
        self.shape = Shape(m=len(mat), n=s)

    def __getitem__(
        self, key: int | slice | EllipsisType | tuple[int | slice | EllipsisType]
    ) -> Any | 'Matrix' | NoReturn:
        '''
        Index from 1 to m, from 1 to n\n
        - If int, return an element in a row or column vector, or a row in a general Matrix\n
        - If slice, always return a Matrix\n
            - If self.shape.m == 1, return a row vector\n
            - Else, return a Matrix of rows\n
        - If Ellipsis, return a copy\n
        - If tuple, return an element or a Matrix\n
            - One row:\n
                - One column, return an element\n
                - Slice columns, return a row vector\n
                - Ellipsis, return a row\n
            - Slice rows:\n
                - One column, return a column vector\n
                - Slice columns, return a general Matrix\n
                - Ellipsis, return a Matrix of rows\n
            - Ellipsis:\n
                - One column, return a coulumn\n
                - Slice columns, return a Matrix of columns\n
                - Ellipsis, return a copy\n
        - Default, TypeError
        '''
        # If int, return an element in a row or column vector, or a row in a general Matrix
        if isinstance(key, int):
            if self.shape.m == 1:
                return self.mat[0][key-1]
            elif self.shape.n == 1:
                return self.mat[key-1][0]
            else:
                return Matrix([self.mat[key-1][:]])

        # If slice, always return a Matrix
        elif isinstance(key, slice):
            if key.start:
                key = slice(key.start-1, key.stop, key.step)
            if key.stop:
                key = slice(key.start, key.stop-1, key.step)
            # If m == 1, return a row vector
            if self.shape.m == 1:
                return Matrix([self.mat[0][key]])

            # Else, return a Matrix of rows
            else:
                return Matrix([_[:] for _ in self.mat[key]])

        # If Ellipsis, return a copy
        elif key == Ellipsis:
            return Matrix([_[:] for _ in self.mat])

        # If tuple, return an element or a Matrix
        elif isinstance(key, tuple):
            key = list(key)
            # One row:
            if isinstance(key[0], int):
                # One column, return an element
                if isinstance(key[1], int):
                    return self.mat[key[0]-1][key[1]-1]

                # Slice columns, return a row vector
                elif isinstance(key[1], slice):
                    if key[1].start:
                        key[1] = slice(key[1].start-1, key[1].stop, key[1].step)
                    if key[1].stop:
                        key[1] = slice(key[1].start, key[1].stop-1, key[1].step)
                    return Matrix([self.mat[key[0]-1][key[1]]])

                # Ellipsis, return a row
                elif key[1] == Ellipsis:
                    return Matrix([self.mat[key[0]-1][:]])

                # Default, TypeError
                else:
                    raise TypeError

            # Slice rows:
            elif isinstance(key[0], slice):
                if key[0].start:
                    key[0] = slice(key[0].start-1, key[0].stop, key[0].step)
                if key[0].stop:
                    key[0] = slice(key[0].start, key[0].stop-1, key[0].step)
                # One column, return a column vector
                if isinstance(key[1], int):
                    temp: list[list] = []
                    for i in range(self.shape.m)[key[0]]:
                        temp.append([self.mat[i][key[1]-1]])
                    return Matrix(temp)

                # Slice columns, return a general Matrix
                elif isinstance(key[1], slice):
                    if key[1].start:
                        key[1] = slice(key[1].start-1, key[1].stop, key[1].step)
                    if key[1].stop:
                        key[1] = slice(key[1].start, key[1].stop-1, key[1].step)
                    temp: list[list] = []
                    flag = 0
                    for i in range(self.shape.m)[key[0]]:
                        temp.append([])
                        for j in range(self.shape.n)[key[1]]:
                            temp[flag].append(self.mat[i][j])
                        flag += 1
                    return Matrix(temp)

                # Ellipsis, return a Matrix of rows
                elif key[1] == Ellipsis:
                    return Matrix([_[:] for _ in self.mat[key[0]]])

                # Default, TypeError
                else:
                    raise TypeError

            # Ellipsis:
            elif key[0] == Ellipsis:
                # One column, return a coulumn
                if isinstance(key[1], int):
                    temp: list[list] = []
                    for i in range(self.shape.m):
                        temp.append(self.mat[i][key[1]-1])
                    return Matrix(temp)

                # Slice columns, return a Matrix of columns
                elif isinstance(key[1], slice):
                    if key[1].start:
                        key[1] = slice(key[1].start-1, key[1].stop, key[1].step)
                    if key[1].stop:
                        key[1] = slice(key[1].start, key[1].stop-1, key[1].step)
                    temp: list[list] = []
                    flag = 0
                    for i in range(self.shape.m):
                        temp.append([])
                        for j in range(self.shape.n)[key[1]]:
                            temp[flag].append(self.mat[i][j])
                        flag += 1
                    return Matrix(temp)

                # Ellipsis, return a copy
                elif key[1] == Ellipsis:
                    return Matrix([_[:] for _ in self.mat])

                # Default, TypeError
                else:
                    raise TypeError

            # Default, TypeError
            else:
                raise TypeError

        # Default, TypeError
        else:
            raise TypeError

    def __setitem__(
        self, key: int | slice | EllipsisType | tuple[int | slice | EllipsisType],
        value: Any
    ) -> NoReturn:
        '''
        Index from 1 to m, from 1 to n
        '''
        # If int
        if isinstance(key, int):
            if self.shape.m == 1:
                self.mat[0][key-1] = value
            elif self.shape.n == 1:
                self.mat[key-1][0] = value
            else:
                for i in range(self.shape.n):
                    self.mat[key-1][i] = value

        # If slice
        elif isinstance(key, slice):
            if key.start:
                key = slice(key.start-1, key.stop, key.step)
            if key.stop:
                key = slice(key.start, key.stop-1, key.step)
            if self.shape.m == 1:
                for i in range(self.shape.n)[key]:
                    self.mat[0][i] = value

            else:
                for i in range(self.shape.m)[key]:
                    for j in range(self.shape.n):
                        self.mat[i][j] = value

        # If Ellipsis
        elif key == Ellipsis:
            for i in range(self.shape.m):
                for j in range(self.shape.n):
                    self.mat[i][j] = value

        # If tuple, return an element or a Matrix
        elif isinstance(key, tuple):
            key = list(key)
            # One row:
            if isinstance(key[0], int):
                # One column
                if isinstance(key[1], int):
                    self.mat[key[0]-1][key[1]-1] = value

                # Slice columns
                elif isinstance(key[1], slice):
                    if key[1].start:
                        key[1] = slice(key[1].start-1, key[1].stop, key[1].step)
                    if key[1].stop:
                        key[1] = slice(key[1].start, key[1].stop-1, key[1].step)
                    for i in range(self.shape.n)[key[1]]:
                        self.mat[key[0]-1][i] = value

                # Ellipsis
                elif key[1] == Ellipsis:
                    for i in range(self.shape.n):
                        self.mat[key[0]-1][i] = value

                # Default, TypeError
                else:
                    raise TypeError

            # Slice rows:
            elif isinstance(key[0], slice):
                if key[0].start:
                    key[0] = slice(key[0].start-1, key[0].stop, key[0].step)
                if key[0].stop:
                    key[0] = slice(key[0].start, key[0].stop-1, key[0].step)
                # One column
                if isinstance(key[1], int):
                    for i in range(self.shape.m)[key[0]]:
                        self.mat[i][key[0]-1] = value

                # Slice columns
                elif isinstance(key[1], slice):
                    if key[1].start:
                        key[1] = slice(key[1].start-1, key[1].stop, key[1].step)
                    if key[1].stop:
                        key[1] = slice(key[1].start, key[1].stop-1, key[1].step)
                    for i in range(self.shape.m)[key[0]]:
                        for j in range(self.shape.n)[key[1]]:
                            self.mat[i][j] = value

                # Ellipsis
                elif key[1] == Ellipsis:
                    for i in range(self.shape.m)[key[0]]:
                        for j in range(self.shape.n):
                            self.mat[i][j] = value

                # Default, TypeError
                else:
                    raise TypeError

            # Ellipsis:
            elif key[0] == Ellipsis:
                # One column
                if isinstance(key[1], int):
                    for i in range(self.shape.m):
                        self.mat[i][key[1]-1] = value

                # Slice columns
                elif isinstance(key[1], slice):
                    if key[1].start:
                        key[1] = slice(key[1].start-1, key[1].stop, key[1].step)
                    if key[1].stop:
                        key[1] = slice(key[1].start, key[1].stop-1, key[1].step)
                    for i in range(self.shape.m):
                        for j in range(self.shape.n)[key[1]]:
                            self.mat[i][j] = value

                # Ellipsis
                elif key[1] == Ellipsis:
                    for i in range(self.shape.m):
                        for j in range(self.shape.n):
                            self.mat[i][j] = value

                # Default, TypeError
                else:
                    raise TypeError

            # Default, TypeError
            else:
                raise TypeError

        # Default, TypeError
        else:
            raise TypeError

    def __add__(self, other: 'Matrix') -> 'Matrix':
        if self.shape != other.shape:
            raise ValueError('Wrong shape')
        temp: list[list] = []
        for i in range(self.shape.m):
            temp.append([])
            for j in range(self.shape.n):
                temp[-1].append(self[i+1, j+1]+other[i+1, j+1])
        return Matrix(temp)

    def __sub__(self, other: 'Matrix') -> 'Matrix':
        if self.shape != other.shape:
            raise ValueError('Wrong shape')
        temp: list[list] = []
        for i in range(self.shape.m):
            temp.append([])
            for j in range(self.shape.n):
                temp[-1].append(self[i+1, j+1]-other[i+1, j+1])
        return Matrix(temp)

    def __mul__(self, other: Any) -> 'Matrix':
        temp: list[list] = []
        for i in range(self.shape.m):
            temp.append([])
            for j in range(self.shape.n):
                temp[-1].append(self[i+1, j+1]*other)
        return Matrix(temp)

    def __rmul__(self, other: Any) -> 'Matrix':
        temp: list[list] = []
        for i in range(self.shape.m):
            temp.append([])
            for j in range(self.shape.n):
                temp[-1].append(other*self[i+1, j+1])
        return Matrix(temp)

    def __matmul__(self, other: 'Matrix') -> 'Matrix':
        if self.shape.n != other.shape.m:
            raise ValueError('Wrong shape')

        def f(a: int, b: int) -> Any:
            l = []
            for i in range(self.shape.n):
                try:
                    l.append(self[a, i+1]*other[i+1, b])
                except:
                    l.append(self[a, i+1]@other[i+1, b])
            return sum(l)

        temp: list[list] = []
        for i in range(self.shape.m):
            temp.append([])
            for j in range(other.shape.n):
                temp[-1].append(f(i+1, j+1))
        return Matrix(temp)

    def __str__(self) -> str:
        '''
        To print the Matrix
        '''
        s = '['
        for i in range(self.shape.m):
            s += '['
            for j in range(self.shape.n):
                s += str(self.mat[i][j])
                if j != self.shape.n-1:
                    s += ', '
            s += ']'
            if i != self.shape.m-1:
                s += ',\n'
        s += ']'
        return s

    def __len__(self) -> int:
        '''
        To get the shape
        '''
        return self.shape.m*self.shape.n

    def __iter__(self) -> Iterator:
        '''
        An Iterator first left to right then up to down
        '''
        temp_list = []
        for i in range(self.shape.m):
            for j in range(self.shape.n):
                temp_list.append(self.mat[i][j])
        return iter(temp_list)

    def __reversed__(self) -> Iterator:
        '''
        An Iterator first right to left then down to up
        '''
        return iter(self[::-1, ::-1])

    def T(self) -> 'Matrix':
        '''
        Return the transposition Matrix
        '''
        temp: list[list] = []
        for j in range(self.shape.n):
            temp.append([])
            for i in range(self.shape.m):
                temp[j].append(self.mat[i][j])
        return Matrix(temp)

    def enblock(self, row_block: list[int], column_block: list[int]) -> 'Matrix':
        '''
        Enblock matrix according to the /row_block/ and /column_block/\n
        ---\n
        Mat=\n
        [[0, 1, 2],\n
        [3, 4, 5]],\n
        row_block=[1, 1],\n
        column_block=[1, 2]\n
        ->\n
        [[0, Mat_1],\n
        [3, Mat_2]],\n
        Mat_1=[[1, 2]],\n
        Mat_2=[[4, 5]]
        '''
        temp: list[list] = []
        row_start = 1
        column_start = 1
        for x in row_block:
            temp.append([])
            for y in column_block:
                if x == 1 and y == 1:
                    temp[-1].append(self[row_start, column_start])
                else:
                    temp[-1].append(self[row_start:row_start+x, column_start:column_start+y])
                column_start += y
            column_start = 1
            row_start += x
        return Matrix(temp)


# Test
if __name__ == '__main__':
    a = Matrix([[0, 1, 2], [3, 4, 5]])
    print('__getitem__ test:')
    print(a[::-1, ::-1], '\n')
    a[1, ...] = -1
    print('__setitem__ test:')
    print(a, '\n')
    b = Matrix([[1], [2], [3]])
    print('vector __getitem__ test:')
    print(b[2:], '\n')
    b[:3] = 0
    print('vector __setitem__ test:')
    print(b, '\n')
    print('__len__ test:')
    print(len(a), '\n')
    print('self.T test:')
    print(a.T(), '\n')
    print('vector self.T test:')
    print(b.T(), '\n')
    c = a.enblock([1, 1], [1, 2])
    print('enblock test:')
    print(c[1, 1], c[1, 2])
    print(c[2, 1], c[2, 2], '\n')
    print('__iter__ test:')
    print(-1 in a, 6 in a, '\n')
    print('__reversed__ test:')
    print([_ for _ in reversed(a)], '\n')
    d = Matrix([[1, 3, 2], [4, 0, 1]])
    e = Matrix([[1, 3], [0, 1], [5, 2]])
    f = Matrix([[1, 2, 3], [4, 5, 6]])
    print('__add__ test:')
    print(d+f, '\n')
    print('__sub__ test:')
    print(d-f, '\n')
    print('__mul__ & __rmul__ test:')
    print(f*4)
    print(4*f, '\n')
    print('__matmul__ test:')
    print(d@e, '\n')
