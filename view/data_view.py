# -*- coding:utf-8 -*-
import decimal
import json
import time
from flask import Blueprint, request, render_template

from config import db

from dbmodel.userMovie import MovieName, Ranking, Ratings, Movies

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
    if request.method == 'GET':
        return render_template("index.html")
    else:
        global Uid
        Uid = request.form.get('id')
        return render_template("getRecommendMovie.html")


@data.route('/tag', methods=['GET', 'POST'])
def get_tag():
    global tag
    tag = request.form.get('tag')
    return render_template("getTagMovie.html")


@data.route('/Uid', methods=['GET'])
def return_Uid():
    return Uid


@data.route('/tag/getTag', methods=['GET'])
def return_tag():
    return tag


@data.route('/uploadRating', methods=['GET', 'POST'])
def get_rating():
    if request.method == 'GET':
        return render_template("getRecommendMovie.html")
    else:
        userId = request.form.get('uid')
        movieId = request.form.get('movieId')
        rating = request.form.get('rating')
        timestamp = int(time.time())

        if not movieId.isdigit():
            return '请输入正确的电影id<br><a href="javascript:history.go(-1)">返回上一页</a>'
        elif not isFloat(rating):
            return '请输入正确的评分：（0-5之间）<br><a href="javascript:history.go(-1)">返回上一页</a>'
        else:
            rData = Ratings(userId=userId, movieId=movieId, rating=rating, timestamp=timestamp)
            db.session.add(rData)
            db.session.commit()
            print("write to table: ratings")
            print(rData.userId, rData.movieId, rData.rating, rData.timestamp)
            return render_template("index.html")


@data.route('/getMovieName', methods=['GET'])
def get_movie_name():
    data = db.session.query(MovieName).filter(MovieName.userId == Uid).all()
    view_data = {"movieId": [], "movieName": [], "rating": []}

    def build_view_data(item):
        view_data["movieId"].append(item.movieId)
        view_data["movieName"].append(item.movieName)
        view_data["rating"].append(item.rating)

    for item in data:
        build_view_data(item)

    view_data_json = json.dumps(view_data, cls=DecimalEncoder, ensure_ascii=False)

    return view_data_json


@data.route('/getTagMovie', methods=['GET'])
def get_tag_movie():
    data = db.session.query(Movies).filter(Movies.genres.like("%" + tag + "%")).limit(100)
    view_data = {"movieId": [], "title": []}

    def build_view_data(item):
        view_data["movieId"].append(item.movieId)
        view_data["title"].append(item.title)

    for item in data:
        build_view_data(item)

    view_data_json = json.dumps(view_data, cls=DecimalEncoder, ensure_ascii=False)

    return view_data_json


@data.route('/getMovieRanking', methods=['GET'])
def get_movie_ranking():
    data = db.session.query(Ranking).order_by(Ranking.average_rating.desc()).limit(100)
    view_data = {"movieId": [], "movieName": [], "average_rating": []}

    def build_view_data(item):
        view_data["movieId"].append(item.movieId)
        view_data["movieName"].append(item.movieName)
        view_data["average_rating"].append(item.average_rating)

    for item in data:
        build_view_data(item)

    view_data_json = json.dumps(view_data, cls=DecimalEncoder, ensure_ascii=False)

    return view_data_json
