import copy
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
            line = int(i['Line']) - 2
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
    read_file = pd.read_excel(file_obj)
    read_file.to_csv(new_csv_file, index=None, header=True)
    print(str(new_csv_file))

def csv_to_excel(file_path):
    file_obj = pathlib.Path(file_path)
    file_dir = file_obj.parent

    print(file_obj)

    new_csv_file = file_dir / f'{file_obj.with_suffix("").stem}.xlsx'
    read_file = pd.read_csv(file_obj, encoding='UTF-16',)
    read_file.to_excel(new_csv_file, index=None, header=True)
    print(str(new_csv_file))


def not_create_data(data_file, exist_data_file):
    data_file_obj = pathlib.Path(data_file)
    exist_data_file = pathlib.Path(exist_data_file)

    file_dir = data_file_obj.parent
    if not data_file_obj.exists() or not exist_data_file.exists():
        raise Exception("File does not exist.")

    # df_data = pd.read_csv(data_file_obj)
    df_data = pd.read_csv(data_file_obj, encoding='cp1252')

    email_list = []
    with open(exist_data_file, encoding='utf-8') as fp:
        reader = csv.DictReader(fp)
        for i in reader:
            email = i['Company User Email (Required)']
            email_list.append(email)

    index_list = []
    for index, row in df_data.iterrows():
        email = row['Company User Email (Required)']
        if email not in email_list:
            index_list.append(index)

    df_data = df_data.iloc[index_list]
    file_name = file_dir / 'not_create_data.csv'
    df_data.to_csv(file_name, index=False)


def combine_company_and_user(company_file, user_file, address_file):
    company_file_obj = pathlib.Path(company_file, )
    user_file_obj = pathlib.Path(user_file)
    address_file_obj = pathlib.Path(address_file)

    file_dir = company_file_obj.parent
    if not company_file_obj.exists() or not user_file_obj.exists():
        raise Exception("File does not exist.")

    df_company = pd.read_csv(company_file_obj, encoding='cp1252')
    df_user = pd.read_csv(user_file_obj, encoding='cp1252')
    df_address = pd.read_csv(address_file_obj, encoding='cp1252')


    company_list_map = {}
    for index, row in df_company.iterrows():
        company_external_id = row['externalID (Optional)']
        company_list_map[company_external_id] = row

    missing_company_address = []
    address_list = []
    for index, row in df_address.iterrows():
        company_external_id = row['Company External Id']
        if company_external_id not in company_list_map.keys():
            missing_company_address.append(index)
        else:
            company_row = company_list_map[company_external_id]
            row['Customer Group ID (Required)'] = company_row['Customer Group ID (Optional)']
            address_list.append(index)


    missing_company_user = []
    user_result = []
    for index, row in df_user.iterrows():
        company_external_id = row['Company External Id']
        if company_external_id not in company_list_map.keys():
            missing_company_user.append(index)
            continue

        company_row = company_list_map[company_external_id]
        company_row = copy.deepcopy(company_row)
        company_row['Company User Email (Required)'] = row['Email']
        company_row['Company User First Name (Required)'] = row['First Name']
        company_row['Company User Last Name (Required)'] = row['Last Name']
        company_row['Company User Role (Optional)'] = row['Role']
        user_result.append(company_row)

    pd.DataFrame(user_result).to_csv(file_dir / 'new_user.csv', index=False)
    df_user.iloc[missing_company_user].to_csv(file_dir / 'miss_company_user.csv', index=False)
    df_address.iloc[address_list].to_csv(file_dir / 'new_address.csv', index=False)
    df_address.iloc[missing_company_address].to_csv(file_dir / 'miss_company_address.csv', index=False)


def open_file_test(file_path='/mnt/data/test/tmp2.py'):
    file_obj = pathlib.Path(file_path)
    file_dir = file_obj.parent

    f = file_obj.open('rb')
    print()


if __name__ == '__main__':
    fire.Fire()
