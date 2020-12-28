# -*- coding:utf-8 -*-
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext

import math

appName = "spark"  # 你的应用程序名称
master = "local"  # 设置单机
conf = SparkConf().setAppName(appName).setMaster(master)  # 配置SparkContext
sc = SparkContext(conf=conf)

# textFile读取外部数据
rdd = sc.textFile("../data/ratings.csv")  # 以行为单位读取外部文件，并转化为RDD

# 获取数据中的电影id和平均评分
rdd1 = rdd.map(lambda x: (x.split(",")[1], x.split(",")[2])) \
    .filter(lambda x: x[0] != "movieId") \
    .map(lambda x: (x[0], (float(x[1]), 1))) \
    .reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1])) \
    .map(lambda x: (x[0], round(x[1][0] / x[1][1], 1)))

print(rdd1.collect())
