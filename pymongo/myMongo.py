# coding:utf-8

from pymongo import MongoClient
client = MongoClient()
# client = MongoClient("mongodb://mongodb0.example.net:27019")
db = client('testDB')
