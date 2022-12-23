class Shape(object):
        '''Embedded class, may not use it'''
        def __init__(self, m:int, n:int):
            self.m=m
            self.n=n

class Matrix(object):
    '''Members are /mat/, /shape.m/, /shape.n/ and /block/\n
    Methods are /element/, /row/, /column/'''
    def __init__(self, mat:list[list]):
        '''Automatically, we will count the shape and block\n
        Members are /mat/, /shape.m/, /shape.n/ and /block/'''
        s=len(mat[0])
        for x in mat:
            if len(x)!=s:
                raise ValueError
        self.mat=mat
        self.shape=Shape(m=len(mat), n=s)
        self.block=0
        for x in mat:
            for y in x:
                if isinstance(y, Matrix):
                    if y.block>self.block:
                        self.block=y.block

    def element(self, i:int, j:int):
        '''Index from 1 to m, from 1 to n'''
        if i<=0 or i>self.shape.m or j<=0 or j>self.shape.n:
            raise IndexError
        return self.mat[i-1][j-1]

    def row(self, i:int):
        '''The row i of it, index from 1 to m'''
        if i<=0 or i>self.shape.m:
            raise IndexError
        return Matrix([a.mat[i-1]])

    def column(self, j:int):
        '''The column j of it, index from 1 to n'''
        if j<=0 or j>self.shape.n:
            raise IndexError
        return Matrix([[x[j-1]] for x in self.mat])

    def __str__(self):
        '''To print the matrix'''
        s='['
        for i in range(self.shape.m):
            s+=str(self.row(i+1).mat[0])
            if i!=self.shape.m-1:
                s+='\n'
        s+=']'
        return s
    
    def enblock(self, row_block:list[int], column_block:list[int]):
        '''Enblock matrix according to the /row_block/ and /column_block/, as:\n
        /#Mat=[[0, 1, 2], [3, 4, 5]], row_block=[1, 1], column_block=[1, 2]\n
        ->[[0, Mat_1], [3, Mat_2]], Mat_1=[[1, 2]], Mat_2=[[4, 5]]#/'''
        #_m=[[None for x in column_block] for y in row_block]
        pass

#Test
if __name__=='__main__':
    a=Matrix([[0, 1, 2], [3, 4, 5]])
    print(a)
    print(a.block)
    print(a.shape.m, a.shape.n)
    print(a.element(1, 1), a.element(2, 3))
    print(a.row(1), a.row(2))
    print(a.column(1), a.column(3))