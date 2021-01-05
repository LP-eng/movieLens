# -*- coding:utf-8 -*-
import decimal
import json
import time
from flask import Blueprint, request, render_template

from config import db

from dbmodel.userMovie import MovieName
from dbmodel.userMovie import Ratings

"""
本视图专门用于处理ajax数据
"""
data = Blueprint('data', __name__)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)


def isFloat(num):
    try:
        num = float(num)
        if 0 <= num <= 5:
            return True
        else:
            return False
    except ValueError:
        return False


@data.route('/', methods=['GET', 'POST'])
def get_id():
    global Uid
    Uid = request.form.get('id')
    return render_template("getData.html")


@data.route('/Uid', methods=['GET'])
def return_Uid():
    return Uid


@data.route('/uploadRating', methods=['GET', 'POST'])
def get_rating():
    if request.method == 'GET':
        return render_template("getData.html")
    else:
        userId = int(Uid)
        movieId = request.form.get('movieId')
        rating = request.form.get('rating')
        timestamp = int(time.time())

        if not movieId.isdigit():
            return '请输入正确的电影id<br><a href="javascript:history.go(-1)">返回上一页</a>'
        elif not isFloat(rating):
            return '请输入正确的评分：（0-5之间）<br><a href="javascript:history.go(-1)">返回上一页</a>'
        else:
            rData = Ratings(userId=userId, movieId=movieId, rating=rating, timestamp=timestamp)
            # db.session.add(rData)
            # db.session.commit()
            print(rData.userId, rData.movieId, rData.rating, rData.timestamp)
            return render_template("getData.html")


@data.route('/getMovieName', methods=['GET'])
def get_movie_name():
    data = db.session.query(MovieName).filter(MovieName.userId == Uid).all()
    view_data = {"movieName": [], "rating": []}

    def build_view_data(item):
        view_data["movieName"].append(item.movieName)
        view_data["rating"].append(item.rating)

    for item in data:
        build_view_data(item)

    view_data_json = json.dumps(view_data, cls=DecimalEncoder, ensure_ascii=False)

    return view_data_json
