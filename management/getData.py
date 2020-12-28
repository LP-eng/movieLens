import pandas as pd;
from sqlalchemy import create_engine

# 初始化数据库连接，得到评分数据
# MySQL的用户：root, 密码:root, 端口：3306,数据库：movie_data
engine = create_engine('mysql+pymysql://root:root@localhost:3306/movie_data_min')
# 查询语句，选出employee表中的所有数据
sql = "select * from ratings;"
# read_sql_query的两个参数: sql语句， 数据库连接
df = pd.read_sql_query(sql, engine)
# 输出employee表的查询结果
print(df)


