from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017')
chicago_car_accidents_db = client['chicago_car_accidents']


daily = chicago_car_accidents_db['days']
weekly = chicago_car_accidents_db['weeks']
monthly = chicago_car_accidents_db['months']

