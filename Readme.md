## 基于小红书用户笔记的百度地图POI数据分析

### 运行环境

- 开发语言：python 3
- 系统：Windows

### 使用说明

#### 1. 安装依赖项

安装requirement依赖

```
pip install -r requirements.txt
```

主要使用了request实现了百度API爬虫，selenium实现了小红书用户笔记爬虫，numpy实现了数学运算，pandas实现了数据存储，folium和matplotlib实现了数据可视化。

#### 2. 程序使用

- [selenium_xhs.py](selenium_xhs.py)

  小红书用户笔记的爬取，爬虫结果在data/xhs.txt

- [request_map.py](request_map.py)

  百度API地点检索的爬取，爬虫结果在data/**.json

-  [data_process.py](data_process.py) 

  数据处理的过程，处理结果在procession/**.csv

-  [data_visualize.py](data_visualize.py) 

  数据可视化的过程，可视化结果在result/heatmap.html和result/POI_analysis.png

#### 3. 结果展示

<img src="C:\Users\wen'zai'hao\AppData\Roaming\Typora\typora-user-images\image-20231115152934681.png" alt="image-20231115152934681" style="zoom:50%;" />

<img src="C:\Users\wen'zai'hao\AppData\Roaming\Typora\typora-user-images\image-20231115153005737.png" alt="image-20231115153005737" style="zoom: 40%;" />

<img src="C:\Users\wen'zai'hao\Desktop\爬虫作业\result\POI_analysis.png" alt="POI_analysis" style="zoom: 60%;" />

