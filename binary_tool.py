

from decimal import Decimal
from math import pow


def get_oct_by_binary(s, m):
    res = Decimal("1")
    index = 0
    for i in s:
        if i == " ":
            continue
        index += 1
        if i == '1':
            res += Decimal(pow(2, -1 * index))
    res = res * Decimal(pow(2, m))
    print(res)
    return res


s1 = "0011001100110011001100110011001100110011001100110100"
a1 = get_oct_by_binary(s1, -2)


def binary_plus(a, b):
    if len(a) != len(b):
        print("length error")
        return
    res = ""
    tmp = 0
    for i in range(len(a)-1, -1, -1):
        if a[i] == ".":
            continue
        x = int(a[i]) + int(b[i]) + tmp
        res += str(x % 2)
        tmp = x // 2
    if tmp:
        res += str(tmp)

    return res[::-1]

xx = binary_plus("0.1100110011001100110011001100110011001100110011001101",
                  "1.1001100110011001100110011001100110011001100110011010"
                  )
get_oct_by_binary(xx, -2)
