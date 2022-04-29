

num_map = [chr(ord('A') + i) for i in range(10)]


def num_to_pattern(num):
    res = []
    for i in range(0, 10):
        h_str = ''
        for j in str(num):
            index = (int(j)+i) % 10
            h_str += num_map[index]
        res.append(h_str)
    return res


print(num_to_pattern(123333))
print(num_to_pattern(12341234))
print(num_to_pattern(131313))
