
import tempfile
import csv


def tmp_file():
    with tempfile.TemporaryFile(mode='w+') as fp:
        order_file_obj = csv.writer(fp)
        orders = [3, 4]
        order_file_obj.writerow(orders)
        fp.seek(0)

        content = fp.read()
    print(content)

def test_dict_csv2():
    header = ['A', 'B', 'C']
    with open('a.csv', mode='w+') as fp:
        file_obj = csv.DictWriter(fp, fieldnames=header)
        file_obj.writeheader()
        data_list = [{
            'A': '1111',
            'B': None,
            'C': 222
        }]
        for data in data_list:
            file_obj.writerow(data)



def test_dict_csv():
    header = ['A', 'B', 'C']
    with open('a.csv', mode='w+') as fp:
        order_file_obj = csv.writer(fp)
        data_list = [[3, None, 4], [None, 'None', ""]]
        for i in data_list:
            order_file_obj.writerow(i)

test_dict_csv()