#coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost:3306/werewolf?charset=utf8mb4'
db = SQLAlchemy(app)
