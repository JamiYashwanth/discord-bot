from pymongo import MongoClient


client = MongoClient('mongodb+srv://19l31a0581:fenA5B7Qr9FtFjw5@cluster0.9mhf5ll.mongodb.net/test')
db = client['contestDetails']
collection = db['ranklists']

def convert_rank_to_number():
    last_operation = system_profile.find().sort('$natural', -1).limit(1)    # print the last command
    # print(last_command)
    # collection.update_many({}, [{'$set': {'Rank': {'$toInt': '$Rank'}}}])

# convert_rank_to_number();