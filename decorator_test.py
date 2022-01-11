import types
from functools import partial, update_wrapper, wraps


class MyDecorator(object):
    def __init__(self, func):
        update_wrapper(self, func)
        self.func = func

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return partial(self.__call__, obj)

    def __call__(self, obj, *args, **kwargs):
        print('Logic here')
        return self.func(obj, *args, **kwargs)


class Profiled:

    def __init__(self, func):
        self.func = func
        wraps(func)(self)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)


class Spam:

    @MyDecorator
    def bar(self, x):
        print(self, x)

        self.abc(9)

    def abc(self, c):
        print(c)


s = Spam()
# print(s)
# print(s.bar)
# print(s.__dict__)
# print(Spam.__dict__)
s.bar(1)
