import os

import pandas as pd


#将所有文件的路径放入到listcsv列表中
def list_dir(file_dir):
    list_csv = []
    dir_list = os.listdir(file_dir)
    for cur_file in dir_list:
        path = os.path.join(file_dir,cur_file)

        #判断是文件夹还是文件
        if os.path.isfile(path):
            dir_files = os.path.join(file_dir, cur_file)

        #判断是否存在.csv文件，如果存在则获取路径信息写入到list_csv列表中
        if os.path.splitext(path)[1] == '.csv':
            csv_file = os.path.join(file_dir, cur_file)
            list_csv.append(csv_file)
        if os.path.isdir(path):
            list_dir(path)
    return list_csv


# 数据处理
# 处理空值，对省份进行排序
def data_process(file_path):
    # 读取数据
    df = pd.read_csv(file_path)

    # 修改列名
    df.rename(columns={
        "dealerName":"经销商名",
        "provinces":"省",
        "city":"城市",
        "address":"地址",
        "salesTel":"销售电话",
        "districtName":"地区",
        "afterSalesTel":"售后电话",
        "businessHours":"营业时间",
        "companyName":"公司全称"
    })

    # 删除所有空列
    df.dropna(axis=1, how='all',inplace=True)
    # print(df.isna().sum(),df.count())

    # 对 'provinces' 列进行降序排序
    df = df.sort_values(by=['provinces','city'], ascending=False)

    # 将修改后的数据覆盖写入原 CSV 文件
    df.to_csv(file_path, index=False, mode='w')



list_dir_csv = list_dir('./')

for i in list_dir_csv:
    data_process(i)

print("数据清洗完成")