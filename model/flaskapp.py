#coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost:3306/werewolfwechat?charset=utf8mb4'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://yz:yz8833757992@@rm-uf6lef7znkjk2kdl2o.mysql.rds.aliyuncs.com:3306/werewolfwechat?charset=utf8mb4'
db = SQLAlchemy(app)
