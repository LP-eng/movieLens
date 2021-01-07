import numpy as np
import pandas as pd
import pymysql

# 连接mysql
from sqlalchemy import create_engine

host = "106.15.193.14"
user = "movie_data"
conn = pymysql.connect(host=host, port=3306, user=user, passwd="root",
                       db="movie_data", charset="utf8")

# 查看需数据
sql_1 = "select * from ratings"  # 写sql查询ratings表
sql_2 = "(select * from movies) tmp"  # 写sql查询movies表

# 得到数据
df = pd.read_sql(sql_1, con=conn)
conn.close()

# 对数据进行操作
df1 = df.drop(columns='timestamp')
rating_dict = {}

# 将数据转换为矩阵‎
for i in range(df1.shape[0]):
    line = df1.iloc[i, :]
    if line.userId in rating_dict:
        rating_dict[int(line.userId)][int(line.movieId)] = float(line.rating)
    else:
        rating_dict[int(line.userId)] = {int(line.movieId): float(line.rating)}

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

# 离线推荐系统
predict_matrix = pd.DataFrame()
userIdlist = rating_matrix.index
movieIdList = rating_matrix.columns
for user in range(rating_matrix.shape[0]):
    userId = userIdlist[user]
    unrate = np.isnan(rating_matrix.values[user, :])
    haverated = ~unrate
    recommendId = movieIdList[unrate]
    similar_movie_rated = (cosSim[unrate, :][:, haverated]) * (cosSim[unrate, :][:, haverated] > 0.4)  # martix of
    ratedmovie = (rating_matrix.values[user, :][haverated])
    print(userIdlist[user])
    sum_rated_cos = np.sum(similar_movie_rated, axis=1)
    for i in range(sum_rated_cos.shape[0]):
        if sum_rated_cos[i] == 0:
            sum_rated_cos[i] = 1
    predict_Val = similar_movie_rated.dot(ratedmovie.T) / sum_rated_cos
    index = np.argsort(predict_Val)[::-1]
    if len(predict_Val > 10):
        index = index[:10]
    predict_Val = predict_Val[index]
    recommendId = recommendId[index]
    predict_matrix = pd.concat(
        [predict_matrix, pd.DataFrame({'userId': userId, 'recommendId': recommendId, 'predictScore': predict_Val})])

# 将其索引值重新改变
predict_matrix.reset_index(inplace=True)
# 创建连接
engine = create_engine('mysql+pymysql://movie_data:root@106.15.193.14:3306/movie_data?charset=utf8')
# 存入数据库
predict_matrix.to_sql(name="user_recommend_movie", con=engine, if_exists="replace", index=True)
