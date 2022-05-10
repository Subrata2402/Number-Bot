from pymongo import MongoClient

data = MongoClient('mongodb+srv://Subrata3250:Subrata@3250@cluster0.ywnwn.mongodb.net/NumberBot?retryWrites=true&w=majority')
db = data.get_database("NumberBot")
user = db.points
