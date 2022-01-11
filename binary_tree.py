class Node:
    def __init__(self, v) -> None:
        self.value = v
        self.left = None
        self.right = None


def pre_print(root):
    res_data = []

    def get_data(root):
        if root:
            res_data.append(root.value)
            get_data(root.left)
            get_data(root.right)
    get_data(root)

    return res_data


def pre_print_for(root):
    res_data = []
    stack = []
    if root:
        WHITE, GRAY = 0, 1
        stack.append((WHITE, root))
        while stack:
            flag, node = stack.pop()
            if not node:
                continue

            if flag == WHITE:
                stack.append((WHITE, node.right))
                stack.append((WHITE, node.left))
                stack.append((GRAY, node))
            if flag == GRAY:
                res_data.append(node.value)

    return res_data


def breadth_print(root):
    queue = []
    res_data = []
    if root:
        queue.append(root)
        while queue:
            node = queue.pop(0)
            if node:
                res_data.append(node.value)
                queue.append(node.left)
                queue.append(node.right)
    return res_data


def depth_print(root):
    stack = []
    res_data = []
    if root:
        stack.append(root)
        while stack:
            node = stack.pop()
            if node:
                res_data.append(node.value)
                stack.append(node.right)
                stack.append(node.left)
    return res_data


def BT_builder(data, i, n):
    if (i < n) and data[i] is not None:
        root = Node(data[i])
        root.left = BT_builder(data, 2*i + 1, n)
        root.right = BT_builder(data, 2*i + 2, n)
        return root
    else:
        return None


in_data = [
    1, 2, 3, 4, None, 5, 6, None, 7, None, None, None, 8
]
# in_data = [
#     0, 1, 2, 3, 4, 5, 6,  7, 8, 9
# ]
r = BT_builder(in_data, 0, len(in_data))


print(pre_print(r))
print(pre_print_for(r))
print("-"*30)
print(breadth_print(r))
print(depth_print(r))

