from pymongo import MongoClient

data = MongoClient('mongodb+srv://Subrata2001:Subrata2001@cluster0.ywnwn.mongodb.net/NumberBot?retryWrites=true&w=majority')
db = data.get_database("NumberBot")
points = db.points