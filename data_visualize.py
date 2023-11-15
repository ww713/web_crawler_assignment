import folium
from folium.plugins import HeatMap
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt


def bMapTransGDMap(lng, lat):
    x_pi = 3.14159265358979324 * 3000.0 / 180.0
    x = np.array(lng) - 0.0065
    y = np.array(lat) - 0.006
    z = np.sqrt(np.power(x, 2) + np.power(y, 2)) - 0.00002 * np.sin(y * x_pi)

    theta = np.arctan2(y, x) - 0.000003 * np.cos(x * x_pi)
    lngs = z * np.cos(theta)
    lats = z * np.sin(theta)

    return lngs, lats


def baidu_to_gd(pd):
    for i in range(len(pd)):
        lngs, lats = bMapTransGDMap(pd.iloc[i]['lng'], pd.iloc[i]['lat'])
        pd.at[i, 'lng'], pd.at[i, 'lat'] = lngs, lats

    return pd


def draw_map(data):
    # 创建地图
    mymap = folium.Map(location=[data['lat'].mean(), data['lng'].mean()],
                       tiles='https://webrd02.is.autonavi.com/appmaptile?lang=zh_en&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
                       attr='高德-常规图', zoom_start=12, control_scale=True)

    # 自定义热力图颜色梯度
    gradient = {0.2: 'blue', 0.4: 'green', 0.6: 'yellow', 0.8: 'red', 1: 'white'}

    # 添加热力图层
    heat_data = [[row['lat'], row['lng'], row['count']] for index, row in data.iterrows()]
    HeatMap(heat_data, radius=15, blur=25, max_zoom=20, gradient=gradient).add_to(mymap)

    # 画一个矩形框 (displayed on the larger area)
    min_lat, max_lat, min_lon, max_lon = 30.685891, 31.880513, 120.861562, 122.141866
    folium.Rectangle(bounds=[(min_lat, min_lon), (max_lat, max_lon)], color='blue', fill=False,
                     fill_opacity=0.2).add_to(mymap)

    # 画一个矩形框 around the specific area
    min_lat, max_lat, min_lon, max_lon = 30.982117, 31.352561, 121.246813, 121.582243
    folium.Rectangle(bounds=[(min_lat, min_lon), (max_lat, max_lon)], color='red', fill=False).add_to(mymap)

    # 显示地图
    mymap.save('result\\heatmap.html')  # 保存为HTML文件
    mymap.show_in_browser()


def POI_analysis(data, raw_data):

    # 提取地址信息和对应的出现次数
    addresses_raw = raw_data['address']
    addresses_data = data[['address', 'count']]

    # 提取行政区划的关键词
    district_keywords = ['黄浦区', '徐汇区', '长宁区', '静安区', '普陀区', '虹口区', '杨浦区', '闵行区', '浦东新区']

    # 初始化计数器
    district_counter_raw = Counter()
    district_counter_data = Counter()

    # 遍历原始数据的地址信息，计数行政区划关键词
    for address in addresses_raw:
        for keyword in district_keywords:
            district_counter_raw[keyword] += address.count(keyword)

    # 遍历处理后数据的地址信息，计数行政区划关键词，并乘以对应的数量
    for index, row in addresses_data.iterrows():
        address = row['address']
        count = row['count']
        for keyword in district_keywords:
            district_counter_data[keyword] += address.count(keyword) * count

    # 将计数结果转换为DataFrame，并按照计数大小排序
    district_df_raw = pd.DataFrame.from_dict(district_counter_raw, orient='index', columns=['Count']).sort_values(by='Count', ascending=False)
    district_df_data = pd.DataFrame.from_dict(district_counter_data, orient='index', columns=['Count']).sort_values(by='Count', ascending=False)

    # 计算两个DataFrame的结果相除
    district_df_ratio = district_df_data / district_df_raw

    # 画图进行分析
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 9))

    district_df_raw.plot(kind='bar', ax=axes[0, 0], legend=False, color='skyblue')
    axes[0, 0].set_title('行政区划POI计数')
    axes[0, 0].set_ylabel('计数')

    district_df_data.plot(kind='bar', ax=axes[0, 1], legend=False, color='salmon')
    axes[0, 1].set_title('行政区划热点POI计数')
    axes[0, 1].set_ylabel('计数')

    district_df_ratio.sort_values(by='Count', ascending=False).plot(kind='bar', ax=axes[1, 0], legend=False, color='green')
    axes[1, 0].set_title('行政区划POI与热点POI计数比例')

    plt.tight_layout()
    plt.savefig('rusult\\POI_analysis.png')
    plt.show()


def main():
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

    # 读取CSV文件
    file_path1 = "procession\\路名信息output.csv"
    file_path2 = "procession\\旅游景点信息output.csv"
    data1 = pd.read_csv(file_path1)
    data2 = pd.read_csv(file_path2)

    file_path3 = "procession\\路名信息.csv"
    file_path4 = "procession\\旅游景点信息.csv"
    data3 = pd.read_csv(file_path3)
    data4 = pd.read_csv(file_path4)

    # 将两个数据框的行连接在一起
    data = pd.concat([data1, data2], ignore_index=True)
    data = baidu_to_gd(data)
    raw_data = pd.concat([data3, data4], ignore_index=True)

    draw_map(data)
    POI_analysis(data, raw_data)


if __name__ == '__main__':
    main()
