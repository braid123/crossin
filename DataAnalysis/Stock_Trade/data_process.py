import pandas as pd


def read_data(file_name):
    """
    读取CSV文件数据并以DataFrame格式返回
    """
    all_data = pd.read_csv(file_name, parse_dates=True, index_col=0)
    return all_data


def read_and_resample_data(file_name, mode, fill_method="ffill"):
    """
    以DataFrame格式读取CSV文件数据后对数据按照工作日重采样
    ffill方式填充缺失数据
    """
    return read_data(file_name).resample(mode, fill_method=fill_method)
