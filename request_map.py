import numpy as np
import requests
import json


def main():
    lat_1 = 30.982117  # Shanghai city lower left latitude
    lon_1 = 121.246813  # Shanghai city lower left longitude
    lat_2 = 31.352561  # Shanghai city upper right latitude
    lon_2 = 121.582243  # Shanghai city upper right longitude

    ak = 'BxLiYsaxxQwY5Y95YMn274ghRM8ROnXe'

    queries = ['道路', '旅游景点']

    for query in queries:
        path = 'data\\'+query+'信息.json'
        f = open(path, 'w+', encoding='utf-8')

        # 经纬度范围设置，按每次偏移两公里来移动检索圆心
        for lat in np.arange(lat_1, lat_2, 0.02):
            for long in np.arange(lon_1, lon_2, 0.02):

                latstr = str(lat)
                longstr = str(long)
                bounds = latstr + ',' + longstr

                # for i in range(len(queries)):
                # query的参数值设为道路，检索半径设置为2公里
                api = "http://api.map.baidu.com/place/v2/search?query={2}&location={0}&radius=2000&output=json&ak={1}".format(bounds, ak, query)
                r = requests.get(api, headers={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'Connection': 'close'}, timeout=(5, 5))

                result = r.json()
                # 是否成功返回结果
                if result['status'] == 0:
                    # 是否包含路况信息
                    results = result['results']
                    if len(results) != 0:
                        for road in results:
                            # 每条路的json文件单独保存
                            print(json.dumps(road, ensure_ascii=False))
                            f.write(json.dumps(road, ensure_ascii=False, indent=4))

    f.close()


if __name__ == '__main__':
    main()
