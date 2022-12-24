'''
The trick of recursion to travel a tree
{
root        # input root node
length=1    # to record the numbers of nodes

def f(node: TreeNode):
    if node.sons == None:
        pass
    else:
        for x in node.sons:

            # processing #

            nonlocal length
            length += 1
        for x in node.sons:
            f(x)

f(root) # recurse
}
'''


class TreeNode(object):
    '''
    index: int = 0,
    sons: list['TreeNode'] = None
    '''

    def __init__(
        self,
        index: int = 0,
        sons: list['TreeNode'] = None
    ):
        self.index = index
        self.sons = sons


def tree2arr(root: TreeNode) -> list[list[bool]]:
    # declare E and |V|
    connect_set = set()
    length = 1

    def f(node: TreeNode):
        if node.sons == None:
            pass
        else:
            for x in node.sons:
                connect_set.add((node.index, x.index))
                connect_set.add((x.index, node.index))
                nonlocal length
                length += 1
            for x in node.sons:
                f(x)

    f(root)
    # declare the adjacency matrix
    arr = []
    for i in range(length):
        temp = []
        for j in range(length):
            temp.append(0)
        arr.append(temp)
    # to construct the adjacency matrix
    for i in range(length):
        for j in range(length):
            if (i, j) in connect_set:
                arr[i][j] = 1
    return arr


def istree(arr: list[list[bool]]) -> bool:
    n = len(arr)
    # Firstly check the diagnal, the diagnal should not have 1
    for i in range(n):
        if arr[i][i]:
            return False
    # Check the connectivity and |E|
    connect_part = {1}
    E_length = 0
    for i in range(n):
        for j in range(i, n):
            if arr[i][j]:
                E_length += 1
                if i+1 in connect_part:
                    connect_part.add(j+1)
    if len(connect_part) != n or E_length != n-1:
        # It means there're at least 2 parts or |E| != |V|-1
        return False
    else:
        return True


def father_code(root: TreeNode) -> list[int]:
    connect_set = set()
    length = 1

    def f(node: TreeNode):
        if node.sons == None:
            pass
        else:
            for x in node.sons:
                connect_set.add((node.index, x.index))
                nonlocal length
                length += 1
            for x in node.sons:
                f(x)

    f(root)
    code = [0]*(length-1)
    for i in range(1, length):
        for j in range(length):
            if (j, i) in connect_set:
                code[i-1] = j   # assign i_{father} to code[i_{son}-1]
                break
    return code


def father_code2tree(code: list[int]) -> TreeNode:
    length = len(code)+1
    nodes = [TreeNode(index=i, sons=[]) for i in range(length)]
    for i in range(length-1):
        nodes[code[i]].sons.append(nodes[i+1])
    return nodes[0]


if __name__ == '__main__':
    root = TreeNode(
        index=0,
        sons=[
            TreeNode(
                index=3,
                sons=[
                    TreeNode(index=1, sons=[]),
                    TreeNode(index=2)
                ]
            )
        ]
    )
    code = father_code(root)
    print(father_code(root))
    root = father_code2tree(code)
    print(root.index)
    root = root.sons[0]
    print(root.index)
    print(root.sons[0].index)
    print(root.sons[1].index)
