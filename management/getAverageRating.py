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
url = 'jdbc:mysql://106.15.193.14:3306/movie_data_min?&useSSL=false'
properties = {'user': 'movie_data_min', 'password': 'root'}
# 查看需数据
table1 = "(select * from ratings) tmp"  # 写sql查询ratings表
table2 = "(select * from movies) tmp"  # 写sql查询movies表


def getAverageRating():
    df = spark.read.jdbc(url=url, table=table1, properties=properties)

    # 获取数据中的电影id和平均评分
    rdd = df.rdd.map(lambda x: (x.movieId, x.rating)) \
        .map(lambda x: (x[0], (float(x[1]), 1))) \
        .reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1])) \
        .map(lambda x: (x[0], round(x[1][0] / x[1][1], 3)))

    # 得到电影的平均评分的list
    movie_average_rating = rdd.collect()

    # 获得电影id-电影名
    df2 = spark.read.jdbc(url=url, table=table2, properties=properties)
    movieName = df2.rdd.map(lambda x: (x.movieId, x.title)).collectAsMap()

    # 得到(电影id, 电影名称, 平均评分)
    list_data = []
    for item in movie_average_rating:
        element = {"movieId": item[0], "movieName": movieName[item[0]], "average_rating": item[1]}
        list_data.append(element)

    pd_df = pd.DataFrame(list_data)
    # 将pd的DataFrame转换成spark的DataFrame
    spark_df = spark.createDataFrame(pd_df, schema=["movieId", "movieName", "average_rating"])

    # 给spark_df新增一列索引
    spark_df1 = spark_df.withColumn("id", monotonically_increasing_id()).orderBy("average_rating")
    # 将数据写入数据库
    spark_df1.write.jdbc(url, "movie_average_rating", mode="overwrite", properties=properties)
    spark.stop()
    # timer = threading.Timer(86400, get_data())
    # timer.start()


if __name__ == "__main__":
    getAverageRating()
