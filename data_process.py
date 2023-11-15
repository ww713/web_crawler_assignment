import json
import pandas as pd
from collections import Counter


def json_to_df(path):
    with open(path, 'r', encoding='utf8') as f:
        data = f.read()

    # 将字符串分割成单独的对象
    json_str_list = data.split('}{')
    json_str_list[0] = json_str_list[0].lstrip('{')
    json_str_list[-1] = json_str_list[-1].rstrip('}')

    json_str_list = ["{{{}}}".format(json_str) for json_str in json_str_list]
    data_list = [json.loads(json_str) for json_str in json_str_list]

    for data in data_list:
        # 展开嵌套的字典
        data['lat'] = data['location']['lat']
        data['lng'] = data['location']['lng']
        del data['location']

    df = pd.DataFrame(data_list)
    df = df[['name', 'address', 'lng', 'lat']]

    return df


def main():
    # 读取txt文本
    with open(r'data\\xhs.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    # 读取json文件
    queries = ['道路', '旅游景点']

    for query in queries:
        path = query + '信息.json'
        df = json_to_df(path)
        df.to_csv('procession\\'+query+'.csv', index=False, encoding='utf-8')

        # 获取CSV文件中的关键词列表
        csv_keywords = df['name'].astype(str).tolist()

        # 在文本中计数每个关键词的出现次数
        keyword_counts = Counter()
        for keyword in csv_keywords:
            keyword_counts[keyword] = text.count(keyword)

        # 将计数结果添加到CSV文件中
        df['count'] = df['name'].map(keyword_counts)

        # 过滤计数为零的行
        df_filtered = df[df['count'] > 0]
        df_filtered = df_filtered.sort_values(by='count', ascending=False)
        df_filtered.drop_duplicates(inplace=True)

        # 打印结果
        print("CSV关键词计数:")
        print(df_filtered[['name', 'count']].to_string(index=False))

        # 保存修改后的CSV文件
        df_filtered.to_csv('procession\\'+query+'output.csv', index=False, encoding='utf-8')


if __name__ == '__main__':
    main()
