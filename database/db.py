from pymongo import MongoClient

data = MongoClient('mongodb+srv://Subrata3250:subrata3250@cluster0.gqwt8.mongodb.net/NumberStore?retryWrites=true&w=majority')
db = data.get_database("NumberStore")
user = db.points
