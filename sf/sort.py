

DATA = [
    1, 3, 5, 7, 6, 4, 2, 8, 9, 0
]


def swap(data, i, j):
    data[i], data[j] = data[j], data[i]


def bubble_sort(data, reverse=False):
    cnt = len(data)
    for i in range(cnt-1, 0, -1):
        for j in range(i):
            if reverse and data[j] < data[j+1]:
                swap(data, j, j+1)
            if not reverse and data[j] > data[j+1]:
                swap(data, j, j+1)
    return data


# print(bubble_sort(DATA, True))


def selection_sort(data, reverse=False):
    cnt = len(data)
    for i in range(cnt-1):
        for j in range(i+1, cnt):
            if not reverse and data[i] > data[j]:
                swap(data, i, j)
            if reverse and data[i] < data[j]:
                swap(data, i, j)
    return data


# print(selection_sort(DATA,True))

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


print(insert_sort(DATA, True))



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


print(quick_sort(DATA, True))
