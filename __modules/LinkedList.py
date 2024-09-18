
__author__ = 'asdawej'


class Node(object):
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

    def connect(self, other):
        '''Make two `Node` as one linkedlist(maybe a loop)'''
        if not isinstance(other, Node):
            raise TypeError
        self.next = other

    def search(self, index: int):
        '''Start from `self`, search according `index`'''
        if not isinstance(index, int):
            raise TypeError
        elif index < 0:
            raise IndexError
        i = 0
        s = self
        while i != index:
            i += 1
            s = s.next
            if s is None:
                raise IndexError
        return s.data

    def sum(self, index: int):
        '''Count sum from `self` to the `Node` of `index`'''
        if not isinstance(index, int):
            raise TypeError
        elif index < 0:
            raise IndexError
        ss = self
        s = ss.data
        i = 0
        while i != index:
            i += 1
            ss = ss.next
            s += ss.data
            if s is None:
                raise IndexError
        return s

    if __name__ == '__main__':
        print('LinkedList.Node by ' + __author__)


class BiNode(object):
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def connect(self, other, end: bool):
        '''Connect a `BiNode` to this `BiNode`'s one end, `False` means `left`, `True` means `right`'''
        if (not isinstance(other, BiNode)) or (not isinstance(end, bool)):
            raise TypeError
        if end:
            self.right = other
        else:
            self.left = other

    def search(self, index: list[bool]):
        '''Start from `self`, search according `index`
        \n`index` means a list with `True` or `False`, `False` means `left`, `True` means `right`'''
        s = self
        while index != []:
            i = index[0]
            if not isinstance(i, bool):
                raise TypeError
            s = s.right if i else s.left
            index.pop(0)
            if s is None:
                raise IndexError
        return s.data

    if __name__ == '__main__':
        print('LinkedList.BiNode by ' + __author__)


if __name__ == '__main__':
    a = BiNode(0)
    b = BiNode(1)
    c = BiNode(2)
    a.connect(b, True)
    a.connect(c, False)
    print(a.left.data, a.right.data)
