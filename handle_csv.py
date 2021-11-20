import pathlib
import csv
import fire
import pandas as pd


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

    df = pd.read_csv(data_file_obj)

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


if __name__ == '__main__':
    # combine_error_file('/mnt/data/1.csv',
    #                    '/mnt/data/invalidation_company_import_oov9d9k3v8.csv')
    fire.Fire()
