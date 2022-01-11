

class Node:
    def __init__(self, v) -> None:
        self.value = v
        self.next = None


def Josephus(n, m):
    first = head = Node(0)
    for i in range(1, n):
        node = Node(i)
        head.next = node
        head = node
    head.next = first

    head = first
    index = 0

    l = n
    while head.next != head:
        if index == (m-2) % l:
            print(head.next.value)
            head.next = head.next.next
            index = 0
            l -= 1
        else:
            index += 1
        head = head.next
    print(head.value)


Josephus(5, 3)
