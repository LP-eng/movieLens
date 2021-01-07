# -*- coding:utf-8 -*-
from flask import Blueprint, render_template, request

"""
本视图专门用于处理页面
"""
page = Blueprint('page', __name__)


@page.route('/', endpoint="index")
def index():
    return render_template("index_one.html")


@page.route('/first_page', endpoint="first_page")
def first_page():
    return render_template("index.html")
