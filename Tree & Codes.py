'''
The trick of recursion to travel a tree
{
root        # input root node
length=1    # to record the numbers of nodes

def f(node: TreeNode):
    if node.sons == []:
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
    attr:
        index: int = 0,
        sons: list['TreeNode'] = [] (not shared default)
    method:
        __eq__
    '''

    def __init__(
        self,
        index: int = 0,
        sons: list['TreeNode'] = None
    ):
        self.index = index
        if sons is None:
            self.sons = []
        else:
            self.sons = sons

    def __eq__(self, other: 'TreeNode') -> bool:
        self_sons = sorted(self.sons, key=lambda x: x.index)
        other_sons = sorted(other.sons, key=lambda x: x.index)
        if self.index == other.index and self_sons == other_sons:
            return True
        else:
            return False


def tree2arr(root: TreeNode) -> list[list[bool]]:
    # declare E and |V|
    connect_set = set()
    length = 1

    def f(node: TreeNode):
        if node.sons == []:
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
                if i + 1 in connect_part:
                    connect_part.add(j + 1)
    if len(connect_part) != n or E_length != n - 1:
        # It means there're at least 2 parts or |E| != |V|-1
        return False
    else:
        return True


def father_code(root: TreeNode) -> list[int]:
    connect_set = set()
    length = 1

    def f(node: TreeNode):
        if node.sons == []:
            pass
        else:
            for x in node.sons:
                connect_set.add((node.index, x.index))
                nonlocal length
                length += 1
            for x in node.sons:
                f(x)

    f(root)
    code = [0] * (length - 1)
    for i in range(1, length):
        for j in range(length):
            if (j, i) in connect_set:
                code[i - 1] = j   # assign i_{father} to code[i_{son}-1]
                break
    return code


def father_code2tree(code: list[int]) -> TreeNode:
    length = len(code) + 1
    nodes = [TreeNode(index=i) for i in range(length)]
    for i in range(length - 1):
        nodes[code[i]].sons.append(nodes[i + 1])
    return nodes[0]


def prufer_code(root: TreeNode) -> list[int]:
    mat = tree2arr(root)    # adjacency matrix
    length = len(mat)       # |V|
    pick_set = set()        # store the nodes picked out
    code = []               # store prufer code
    while len(pick_set) != length - 1:
        for i in range(1, length):
            if not i in pick_set:
                connect_num = 0     # degree
                temp_father = 0     # if degree is 1, it will be the true father
                for j in range(length):
                    if not j in pick_set and mat[i][j]:
                        connect_num += 1
                        temp_father = j
                if connect_num == 1:
                    pick_set.add(i)
                    code.append(temp_father)
                    break
    # the end is always 0, so we do not store it
    return code[:-1]


def prufer_code2tree(code: list[int]) -> TreeNode:
    length = len(code) + 2
    aug_code = code + [0]         # add 0 to the end
    nodes = [
        TreeNode(index=i)
        for i in range(length)
    ]
    above_line: list[int] = []  # store the sons
    leaves = [
        i
        for i in range(1, length)
        if not i in aug_code
    ]
    for i in range(length - 1):
        temp = length    # the temp index-min node
        for x in leaves:
            if not x in above_line and not x in aug_code[i:]:
                if x < temp:
                    temp = x
        for x in aug_code[:i]:
            if not x in above_line and not x in aug_code[i:]:
                if x < temp:
                    temp = x
        above_line.append(temp)
    for i in range(length - 1):
        nodes[aug_code[i]].sons.append(nodes[above_line[i]])
    return nodes[0]


class SecondaryNode(object):
    '''
    attr:
        outer: 'SecondaryNode' = None
        inter: 'SecondaryNode' = None
        upper: 'UnionNode' = None
    '''

    def __init__(
        self,
        outer: 'SecondaryNode' = None,
        inter: 'SecondaryNode' = None,
        upper: 'UnionNode' = None
    ):
        self.outer = outer
        self.inter = inter
        self.upper = upper


class UnionNode(object):
    '''
    attr:
        interset: list[SecondaryNode] = [] (not shared default)
    '''

    def __init__(
        self,
        interset: list[SecondaryNode] = None
    ):
        if interset is None:
            self.interset = []
        else:
            self.interset = interset


def UnionNode_connect(
    node1: UnionNode = None,
    node2: UnionNode = None,
    prev1: SecondaryNode = None,
    prev2: SecondaryNode = None,
):
    if node1.interset == []:
        node1.interset.append(SecondaryNode(upper=node1))
        node1.interset[0].inter = node1.interset[0]
        if node2.interset == []:
            node2.interset.append(SecondaryNode(upper=node2))
            node2.interset[0].inter = node2.interset[0]
            node1.interset[0].outer = node2.interset[0]
            node2.interset[0].outer = node1.interset[0]
        else:
            node2.interset.append(
                SecondaryNode(
                    inter=prev2.inter,
                    outer=node1.interset[0],
                    upper=node2
                )
            )
            prev2.inter = node2.interset[-1]
            node1.interset[0].outer = node2.interset[-1]
    else:
        if node2.interset == []:
            node2.interset.append(SecondaryNode(upper=node2))
            node2.interset[0].inter = node2.interset[0]
            node1.interset.append(
                SecondaryNode(
                    inter=prev1.inter,
                    outer=node2.interset[0],
                    upper=node1
                )
            )
            prev1.inter = node1.interset[-1]
            node2.interset[0].outer = node1.interset[-1]
        else:
            node1.interset.append(
                SecondaryNode(
                    inter=prev1.inter,
                    upper=node1
                )
            )
            node2.interset.append(
                SecondaryNode(
                    inter=prev2.inter,
                    upper=node2
                )
            )
            prev1.inter = node1.interset[-1]
            prev2.inter = node2.interset[-1]
            node1.interset[-1].outer = node2.interset[-1]
            node2.interset[-1].outer = node1.interset[-1]


def planar_code(start_node: SecondaryNode) -> list[bool]:
    ptr = start_node.outer              # moving ptr
    path_set = [{start_node, ptr}]      # record the path
    node_set = {start_node, ptr}        # record the nodes
    code: list[bool] = []               # planar code
    while (
        ptr.inter != start_node or
        not ptr.inter.inter in node_set
    ):
        ptr = ptr.inter
        temp_set = {ptr}
        ptr = ptr.outer
        temp_set.add(ptr)
        if temp_set in path_set:
            code.append(0)
        else:
            code.append(1)
            path_set.append(temp_set)
            for x in temp_set:
                node_set.add(x)
    # the start is 1 and the end is 0, ignored
    return code[:-1]


def planar_code2tree(code: list[bool]) -> UnionNode:
    start_node = UnionNode()
    UnionNode_connect(node1=start_node, node2=UnionNode())
    ptr = start_node.interset[0].outer
    for x in code:
        if x:
            UnionNode_connect(
                node1=ptr.upper,
                node2=UnionNode(),
                prev1=ptr
            )
            ptr = ptr.inter.outer
        else:
            ptr = ptr.outer.inter
    return start_node


if __name__ == '__main__':
    # example labeled tree
    root = TreeNode(
        index=0,
        sons=[
            TreeNode(index=1),
            TreeNode(
                index=5,
                sons=[
                    TreeNode(
                        index=4,
                        sons=[
                            TreeNode(index=3)
                        ]
                    ),
                    TreeNode(
                        index=6,
                        sons=[
                            TreeNode(index=2),
                            TreeNode(index=7)
                        ]
                    )
                ]
            )
        ]
    )
    # test father_code()
    print(father_code(root))
    # test father_code2tree()
    print(root == father_code2tree(father_code(root)))
    # test prufer_code()
    print(prufer_code(root))
    # test prufer_code2tree()
    print(root == prufer_code2tree(prufer_code(root)))

    # example unlabeled tree
    tree = [UnionNode() for _ in range(4)]
    UnionNode_connect(
        node1=tree[0],
        node2=tree[1]
    )
    UnionNode_connect(
        node1=tree[0],
        node2=tree[2],
        prev1=tree[0].interset[0]
    )
    UnionNode_connect(
        node1=tree[0],
        node2=tree[3],
        prev1=tree[0].interset[0],
    )
    # test planar_code()
    print(
        planar_code(tree[1].interset[0]),
        planar_code(tree[0].interset[0]),
        planar_code(tree[2].interset[0]),
        planar_code(tree[3].interset[0])
    )
    # test planar_code2tree()
    start = planar_code2tree(planar_code(tree[1].interset[0]))
    print(start.interset)
    print(start.interset[0].outer.upper.interset)
    print(start.interset[0].outer.inter.outer.upper.interset)
    print(start.interset[0].outer.inter.inter.outer.upper.interset)
