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


def get_data():
    # 获取(userId, movieId, rating)的数据格式
    df1 = spark.read.jdbc(url=url, table=table1, properties=properties)
    # rating归一化
    dataRDD = df1.rdd.map(lambda x: (x.userId, x.movieId, x.rating/5))

    # ALS(交替最小二乘)预测 (训练集-数据格式：用户id 物品id 评分(0-1), 根据数据的分散情况测试出来的值
    # 循环次数iter，这个设置的越大肯定是越精确,如果设置很大就可以防止过拟合问题，如果设置很小)
    model = ALS.train(dataRDD, 100, 10, 0.1)

    # 获得电影id-电影名
    df2 = spark.read.jdbc(url=url, table=table2, properties=properties)
    movieName = df2.rdd.map(lambda x: (x.movieId, x.title)).collectAsMap()

    # 获取用户id总人数
    total_user = df1.rdd.map(lambda x: x.userId).distinct().count()

    list_data = []
    for i in range(1, total_user):
        RecommendMovie = model.recommendProducts(i, 10)

        for item in RecommendMovie:
            element = {"userId": item[0], "movieName": movieName[item[1]], "rating": float(item[2])}
            list_data.append(element)

    pd_df = pd.DataFrame(list_data)

    # 将pd的DataFrame转换成spark的DataFrame
    spark_df = spark.createDataFrame(pd_df, schema=["userId", "movieName", "rating"])
    # 给spark_df新增一列索引
    spark_df1 = spark_df.withColumn("id", monotonically_increasing_id())
    # 将数据写入数据库
    spark_df1.write.jdbc(url, "user_recommend_movie", mode="overwrite", properties=properties)
    # timer = threading.Timer(86400, get_data())
    # timer.start()


if __name__ == "__main__":
    get_data()
