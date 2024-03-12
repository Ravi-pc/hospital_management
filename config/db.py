from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/hospital')

db_connection = client['hospital']

