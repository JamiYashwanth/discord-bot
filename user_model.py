from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
print("Connection Successful")

db = client["mydatabase"]
try:
 db.create_collection("users")
except:
    print("already created")

collection = db["users"]

def updateToDb(userName,contestId,contestRank,div,platForm,totalScore,totalTime):
    user_name = userName
    platform = platForm

    contest_details = {
        'contest_id': contestId,
        'contest_rank': contestRank,
        'division': div,
        'total_score' : totalScore,
        'total_time' : totalTime
    }
    # try:
    user = list(collection.find({'user_name': user_name}))
    if (len(user) == 0):
        collection.insert_one({
            'user_name': user_name,
            f'{platform}': [contest_details],
        })
    else:
        checkWhereContestAlreadyExists = list(collection.find({
            'user_name' : user_name,
            f'{platform}.contest_id' : contest_details['contest_id']
        }))
        if(len(checkWhereContestAlreadyExists) == 0):
            collection.update_one({'user_name': user_name}, {'$push': {f'{platform}': contest_details}})
        else:
            collection.update_one({
                'user_name' : user_name,
                f'{platform}.contest_id' : contest_details['contest_id']
            },{
                '$set' : {
                    f'{platform}.$.contest_rank' : contest_details['contest_rank'],
                    f'{platform}.$.division' : contest_details['division'],
                    f'{platform}.$.total_score' : contest_details['total_score'],
                    f'{platform}.$.total_time' : contest_details['total_time']
                }
            })

def userRankings(platForm,userName):
    platform = platForm
    result = list(collection.aggregate([{
        '$match' : {
            'user_name' : userName
        }
    },{
        '$project' : {
            f'{platform}' : 1,
            '_id' : 0
        }
    }]))[0][platform]
    message = ""
    for doc in result:
        message = message + 'Contest : ' + doc['contest_id'] + '\n' +\
                  'Division : ' + doc['division'] + '\n' +\
                  'Rank : ' + doc['contest_rank'] + '\n' +\
                  'Total score : ' + doc['total_score'] + '\n'\
                  'Total time : ' + doc['total_time'] \
                  + "\n\n"
    return message

# client.close()
