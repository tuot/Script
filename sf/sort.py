import time

DATA = [
    1, 3, 5, 7, 6, 4, 2, 8, 9, 0
]


def log_times(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        data = func(*args, **kwargs)
        t = str(time.time() - start)
        print(t)
        return data
    return wrapper


def swap(data, i, j):
    data[i], data[j] = data[j], data[i]


class SortAlgorithm:

    @staticmethod
    def bubble_sort(data, reverse=False):
        cnt = len(data)
        for i in range(cnt-1, 0, -1):
            for j in range(i):
                if reverse and data[j] < data[j+1]:
                    swap(data, j, j+1)
                if not reverse and data[j] > data[j+1]:
                    swap(data, j, j+1)
        return data

    @staticmethod
    def selection_sort(data, reverse=False):
        cnt = len(data)
        for i in range(cnt-1):
            for j in range(i+1, cnt):
                if not reverse and data[i] > data[j]:
                    swap(data, i, j)
                if reverse and data[i] < data[j]:
                    swap(data, i, j)
        return data

    @staticmethod
    def insert_sort(data, reverse=False):
        cnt = len(data)
        for i in range(1, cnt):
            for j in range(i, 0, -1):
                if not reverse:
                    if data[j] < data[j-1]:
                        swap(data, j-1, j)
                    else:
                        break
                if reverse:
                    if data[j] > data[j-1]:
                        swap(data, j-1, j)
                    else:
                        break

        return data

    @staticmethod
    def shell_sort(data, reverse=False):

        l = len(data)
        gap = l // 2

        while gap > 0:
            for i in range(gap):
                for x in range(i, l-gap, gap):
                    for j in range(x+gap, 0, -gap):
                        if not reverse:
                            if data[j] < data[j-gap]:
                                swap(data, j-gap, j)
                            else:
                                break
                        if reverse:
                            if data[j] > data[j-gap]:
                                swap(data, j-gap, j)
                            else:
                                break
            gap = gap // 2

        return data

    @staticmethod
    def quick_sort(data, reverse=False):

        def q_sort(data, start, end):
            ss, ee = start, end
            p = data[start]
            while start < end:
                while start < end:
                    if not reverse:
                        if data[end] < p:
                            swap(data, start, end)
                            break
                        else:
                            end -= 1
                    else:
                        if data[end] > p:
                            swap(data, start, end)
                            break
                        else:
                            end -= 1

                while start < end:
                    if not reverse:
                        if data[start] > p:
                            swap(data, start, end)
                            break
                        else:
                            start += 1
                    else:
                        if data[start] < p:
                            swap(data, start, end)
                            break
                        else:
                            start += 1
            if ss < start-1:
                q_sort(data, ss, start-1)
            if end+1 < ee:
                q_sort(data, end+1, ee)

        q_sort(data, 0, len(data)-1)
        return data

    @staticmethod
    def merge_sort(data, reverse=False):

        def m_sort(data, start, end, reverse):
            if start == end:
                return [data[start]]
            if start + 1 == end:
                if not reverse:
                    if data[start] < data[end]:
                        return data[start], data[end]
                    else:
                        return data[end], data[start]
                else:
                    if data[start] > data[end]:
                        return data[start], data[end]
                    else:
                        return data[end], data[start]
            else:
                mid = (start + end)//2
                left = m_sort(data, start, mid, reverse)
                right = m_sort(data, mid+1, end, reverse)

                res = []
                i, j = 0, 0
                while i < len(left) and j < len(right):
                    if not reverse:
                        while i < len(left) and left[i] <= right[j]:
                            res.append(left[i])
                            i += 1
                        if i >= len(left):
                            while j < len(right):
                                res.append(right[j])
                                j += 1
                        else:
                            while j < len(right) and left[i] > right[j]:
                                res.append(right[j])
                                j += 1
                            if j >= len(right):
                                while i < len(left):
                                    res.append(left[i])
                                    i += 1
                    else:
                        pass
                return res

        return m_sort(data, 0, len(data)-1, reverse)


res = SortAlgorithm.merge_sort([9,8,7,6,5,4,3])
print(res)
