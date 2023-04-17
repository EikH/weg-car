import os

import pandas as pd

# 省份映射字典
province_dict = {
    '北京市': '北京',
    '天津市': '天津',
    '河北省': '河北',
    '山西省': '山西',
    '内蒙古自治区': '内蒙古',
    '辽宁省': '辽宁',
    '吉林省': '吉林',
    '黑龙江省': '黑龙江',
    '上海市': '上海',
    '江苏省': '江苏',
    '浙江省': '浙江',
    '安徽省': '安徽',
    '福建省': '福建',
    '江西省': '江西',
    '山东省': '山东',
    '河南省': '河南',
    '湖北省': '湖北',
    '湖南省': '湖南',
    '广东省': '广东',
    '广西壮族自治区': '广西',
    '海南省': '海南',
    '重庆市': '重庆',
    '四川省': '四川',
    '贵州省': '贵州',
    '云南省': '云南',
    '西藏自治区': '西藏',
    '陕西省': '陕西',
    '甘肃省': '甘肃',
    '青海省': '青海',
    '宁夏回族自治区': '宁夏',
    '新疆维吾尔自治区': '新疆',
    '台湾省': '台湾',
    '香港特别行政区': '香港',
    '澳门特别行政区': '澳门',
    '国外': '国外'
}


# 将所有文件的路径放入到listcsv列表中
def list_dir(file_dir,out_dir):
    csv_files = []
    copy_files = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(root, file))
                copy_files.append(os.path.join(out_dir, file))
    return csv_files,copy_files


# 数据处理
# 处理空值，对省份进行排序
def data_process(file_path,out_path):
    # 读取数据,只保留省，市，经销商名，销售电话
    try:
        df = pd.read_csv(file_path, usecols=["provinces", "city", "dealerName", "salesTel"])
        # 修改列名
        df = df.rename(columns={
            "dealerName": "经销商名",
            "provinces": "省",
            "city": "城市",
            "address": "地址",
            "salesTel": "销售电话",
            "districtName": "地区",
            "afterSalesTel": "售后电话",
            "businessHours": "营业时间",
            "companyName": "公司全称"
        })
    except:
        df = pd.read_csv(file_path, usecols=["省", "城市", "经销商名", "销售电话"])


    # 删除所有空列
    df.dropna(axis=1, how='all', inplace=True)

    # 去重
    df = df.drop_duplicates(subset=['经销商名'])

    # 重排序列顺序
    df = df.reindex(columns=['省', '城市', '经销商名', "销售电话"])

    # 对省份字段进行清洗
    # 对特殊省份处理
    df['省'] = df['省'].replace(province_dict)

    # 创建自定义排序的 Categorical Series
    province_order = ["山东", "江苏", "浙江", "上海", "安徽", "河北", "河南", "北京", "天津", "辽宁", "吉林", "黑龙江",
                      "内蒙古", "湖南", "江西", "广东", "广西", "海南", "福建", "山西", "陕西", "湖北", "四川", "重庆",
                      "贵州", "云南", "新疆", "甘肃", "青海", "西藏", "宁夏"]

    # 将省份列转换为Categorical类型，并按照自定义顺序进行排序
    df['省'] = pd.Categorical(df['省'], categories=province_order, ordered=True)

    # 省份排序完成后对城市进行排序
    df = df.sort_values(['省', '城市'])

    # 将修改后的数据覆盖写入原 CSV 文件
    df.to_csv(out_path, index=False, mode='w')


csv_dirs,csv_out_dirs = list_dir('./源数据','./csv数据')

for i,j in zip(csv_dirs,csv_out_dirs):
    print(i,j)
    data_process(i,j)

print("数据清洗完成")
