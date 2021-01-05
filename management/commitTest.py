import pandas as pd
import numpy as np
import pickle

from pyspark.sql import SparkSession
from pyspark.mllib.recommendation import ALS
import pandas as pd
from pyspark.sql.functions import monotonically_increasing_id

# 连接spark
spark = SparkSession \
    .builder \
    .appName("SparkSQLDemo") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

# 连接mysql
url = 'jdbc:mysql://127.0.0.1:3306/movie_data_min?&useSSL=false'
properties = {'user': 'root', 'password': 'root'}
# 查看需数据
table1 = "(select * from ratings) tmp"  # 写sql查询ratings表
table2 = "(select * from movies) tmp"  # 写sql查询movies表

# 得到协同过滤矩阵
# 获取(userId, {movieId: rating})的数据格式
df1 = spark.read.jdbc(url=url, table=table1, properties=properties)
dataRDD = df1.rdd.map(lambda x: (x.userId, {x.movieId: x.rating})) \
    .reduceByKey(lambda x, y: {**x, **y}) \
    .map(lambda x: {x[0]: x[1]})

# 得到列表
rating_list = dataRDD.collect()
# 将列表转换成字典
rating_dict = {}
for i in rating_list:
    rating_dict = {**rating_dict, **i}
# 将rdd转换成pandas的dataFrame
rating_matrix = pd.DataFrame(rating_dict).T

# 数据规范化，以消除错误‎
rating_matrix3 = ((rating_matrix.T - rating_matrix.T.mean(axis=0)) / (
        rating_matrix.T.max(axis=0) - rating_matrix.T.min(axis=0))).T
rating_matrix_fillzero = rating_matrix3.fillna(0)

# 使用SVD进行分解
U, sigma, Vt = np.linalg.svd(rating_matrix_fillzero)

# 对数据进行降维, 减少有用数据的尺寸，便于计算‎
reduced_matrix = (U[:, :5].dot(np.eye(5) * sigma[:5])).T.dot(rating_matrix_fillzero)

# 规范数据，加快数据预计算‎
std_matrix2 = ((reduced_matrix.T - reduced_matrix.T.mean(axis=0)) / reduced_matrix.T.std(axis=0)).T
# 用于加快相似性的计算‎
std_matrix = std_matrix2

# 计算余弦相似度矩阵 计算相似性
# 分子
upfactor = std_matrix.T.dot(std_matrix)
downfactor = (np.linalg.norm(std_matrix, axis=0).reshape(-1, 1)).dot(np.linalg.norm(std_matrix, axis=0).reshape(1, -1))
# 在原本余弦相似度的基础上进行小小修改，将值定在0～1之间
cosSim = (upfactor / downfactor + 1) / 2


