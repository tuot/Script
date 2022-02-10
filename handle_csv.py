import pathlib
import csv
import fire
import pandas as pd
import time


def split_csv(file_path, split_num):
    file_obj = pathlib.Path(file_path)
    if not file_obj.exists():
        raise Exception("File does not exist.")
    file_dir = file_obj.parent

    df = pd.read_csv(file_path)
    total_rows = len(df)
    split_file_num = total_rows // split_num
    split_file_num += 0 if total_rows % split_num == 0 else 1
    for i in range(0, split_file_num):
        start, end = split_num * i, split_num * (i+1)
        print(start, end)
        df_data = df.iloc[start: end]
        file_name = file_dir / f'{file_obj.with_suffix("").stem} - {i+1}.csv'
        df_data.to_csv(file_name, index=False)


def combine_file(data_file, error_file):
    data_file_obj = pathlib.Path(data_file)
    error_file_obj = pathlib.Path(error_file)

    file_dir = error_file_obj.parent
    if not data_file_obj.exists() or not error_file_obj.exists():
        raise Exception("File does not exist.")

    if data_file_obj.suffix == '.csv':
        df = pd.read_csv(data_file_obj)
    else:
        df = pd.read_excel(data_file_obj)

    error_list = []
    with open(error_file_obj) as fp:
        reader = csv.DictReader(fp)
        df['ErrMsg'] = ''
        for i in reader:
            line = int(i['Line']) -2
            value = i['ErrMsg']
            df.loc[line, 'ErrMsg'] = value
            error_list.append(line)

    df_data = df.iloc[error_list]
    file_name = file_dir / 'new.csv'
    df_data.to_csv(file_name, index=False)

def update_file(data_file, map_file):
    data_file_obj = pathlib.Path(data_file)
    map_file_obj = pathlib.Path(map_file)

    file_dir = map_file_obj.parent
    if not data_file_obj.exists() or not map_file_obj.exists():
        raise Exception("File does not exist.")

    df = pd.read_csv(data_file_obj)

    id_map = {}
    with open(map_file_obj) as fp:
        reader = csv.DictReader(fp)
        for i in reader:
            account_number = i['account_number']
            value = i['bc_id']
            id_map[account_number] = value
    for index, row in df.iterrows():
        account_number = row['account_number (Optional)']
        value = id_map[account_number]
        df.loc[index, 'Customer Group ID (Optional)'] = value

    df_data = df
    file_name = file_dir / 'new.csv'
    df_data.to_csv(file_name, index=False)


def clean_file(data_file):
    data_file_obj = pathlib.Path(data_file)

    file_dir = data_file_obj.parent
    if not data_file_obj.exists():
        raise Exception("File does not exist.")

    df = pd.read_csv(data_file_obj)

    index_list = []
    for index, row in df.iterrows():
        msg = row['ErrMsg']
        if msg == "Email is not correct.":
            continue
        index_list.append(index)

    df_data = df.iloc[index_list]
    file_name = file_dir / 'new.csv'
    df_data.to_csv(file_name, index=False)


def duplicate_data_count(data_file):
    data_file_obj = pathlib.Path(data_file)

    file_dir = data_file_obj.parent
    if not data_file_obj.exists():
        raise Exception("File does not exist.")

    df = pd.read_csv(data_file_obj)

    data_list = []
    email_list = []
    cnt = 0
    for index, row in df.iterrows():
        email = row['Company User Email (Required)'].lower()
        # account_number = row['added so you can find data remove before s ending to Julian']
        # account_number = row['Account Number to Match off of']
        account_number = 0
        key = f'{email},{account_number}'
        if key not in data_list:
            data_list.append(key)
        else:
            cnt += 1
        if email not in email_list:
            email_list.append(email)
    print("duplicate_data:")
    print(len(df.index) - len(data_list))
    print(cnt)
    print("email count:")
    print(len(email_list))

def excel_to_csv(file_path):
    file_obj = pathlib.Path(file_path)
    file_dir = file_obj.parent

    new_csv_file = file_dir / f'{file_obj.with_suffix("").stem}.csv'
    read_file = pd.read_excel (file_obj)
    read_file.to_csv (new_csv_file, index = None, header=True)
    print(str(new_csv_file))



def miss_data(data_file, other_file):
    data_file_obj = pathlib.Path(data_file)
    other_file_obj = pathlib.Path(other_file)

    file_dir = data_file_obj.parent
    if not data_file_obj.exists() or not other_file_obj.exists():
        raise Exception("File does not exist.")

    df_data = pd.read_csv(data_file_obj, low_memory=False)
    df_other_data = pd.read_excel(other_file_obj)

    index_list = []
    miss_email = []
    for index, row in df_other_data.iterrows():
        email = row['Not in BundleB2B or BigCommerce'].lower()
        miss_email.append(email) 

    dd = []
    for index, row in df_data.iterrows():
        email = row['Company User Email (Required)'].lower()
        if email in miss_email:
            index_list.append(index)
            dd.append(email)

    print(set(miss_email) - set(dd))

    df_data = df_data.iloc[index_list]
    file_name = file_dir / f'{int(time.time())}.csv'
    df_data.to_csv(file_name, index=False)


def open_file_test(file_path='/mnt/data/test/tmp2.py'):
    file_obj = pathlib.Path(file_path)
    file_dir = file_obj.parent

    f = file_obj.open('rb')
    print()



if __name__ == '__main__':
    # combine_error_file('/mnt/data/1.csv',
    #                    '/mnt/data/invalidation_company_import_oov9d9k3v8.csv')
    fire.Fire()
