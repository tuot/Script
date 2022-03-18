# 文档实例如下:
from typing import List, TypeVar, Generic

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        # Create an empty list with items of type T
        self.items: List[T] = []

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> T:
        return self.items.pop()

    def empty(self) -> bool:
        return not self.items

stack = Stack[int]()
stack.push(2)
stack.pop()
stack.push('x') # Type error





from decimal import Decimal
from functools import singledispatch
@singledispatch
def fun(arg, verbose=False):
    if verbose:
        print("Let me just say,", end=" ")
    print(arg)


@fun.register
def _(arg: int, verbose=False):
    if verbose:
        print("Strength in numbers, eh?", end=" ")
    print(arg)


@fun.register
def _(arg: list, verbose=False):
    if verbose:
        print("Enumerate this:")
    for i, elem in enumerate(arg):
        print(i, elem)

# 不添加类型形式


@fun.register(complex)
def _(arg, verbose=False):
    if verbose:
        print("Better than complicated.", end=" ")
    print(arg.real, arg.imag)

# 函数形式


def nothing(arg, verbose=False):
    print("Nothing.")


fun.register(type(None), nothing)

# 注册多种值


@fun.register(float)
@fun.register(Decimal)
def fun_num(arg, verbose=False):
    if verbose:
        print("Half of your number:", end=" ")
    print(arg / 2)
