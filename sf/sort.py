

DATA = [
    1, 3, 5, 6, 9, 7, 4, 2, 0, 8
]


def swap(data, i, j):
    data[i], data[j] = data[j], data[i]


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
