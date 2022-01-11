from functools import lru_cache


class A:

    v = -1

    def __init__(self, v) -> None:
        self.v = v

    @classmethod
    @lru_cache(maxsize=128)
    def test(self, a, b):
        print("---in---")
        return self.v + a + b


@lru_cache()
def get_sum(x):
    print("in...")
    return x * x


a = A(1)
print(a.test(1, 2))
b = A(1)
print(b.test(1, 2))

print(a == b)
print(a is b)
