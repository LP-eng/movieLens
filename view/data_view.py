# -*- coding:utf-8 -*-
import decimal
import json
from flask import Blueprint, request, render_template
from config import db

from dbmodel.userMovie import MovieName

"""
本视图专门用于处理ajax数据
"""
data = Blueprint('data', __name__)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)


@data.route('/', methods=['GET', 'POST'])
def get_id():
    global Uid
    Uid = request.form.get('id')
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

    view_data_string = json.dumps(view_data, cls=DecimalEncoder, ensure_ascii=False)

    return view_data_string
