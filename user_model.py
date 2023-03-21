from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np 
import certifi
client = MongoClient('mongodb+srv://19l31a0581:fenA5B7Qr9FtFjw5@cluster0.9mhf5ll.mongodb.net/test', tlsCAFile=certifi.where())
db = client['contestDetails']
collection = db['ranklists']

print("Connection Successful")

# db = client["mydatabase"]
# try:
#  db.create_collection("users")
# except:
#     print("already created")

# collection = db["users"]

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
            'Username' : userName
        }
    }]))
    message = ""
    for doc in result:
        message = message + 'Contest : ' + doc['contest'] + '\n' + 'Division : ' + doc['division'] + '\n' +'Rank : ' +str(doc['Rank'])+ '\n' +'Total score : ' + doc['Total score'] + '\n' + 'Total time : ' + doc['Total time'] + '\n\n'
        if(len(message)>1500):
            break
    return message

# def overallStats(platForm,userName):
#     platform = platForm
#     result = list(collection.aggregate([{
#         '$match' : {
#             'user_name' : userName
#         }
#     },{
#         '$sort' : {
#             f'{platform}.contest_id' : -1
#         }
#     },{
#         '$project' : {
#             f'{platform}.contest_id' : 1,
#             '_id' : 0
#         }
#     }]))[0][platform].sort({'Codechef.contest_rank': 1})
#     print(f'result = {result}')


def graphsGeneration(userName,duration):
    result = list(collection.aggregate([{
        '$match': {
            'Username': userName
        }
    }, {
        '$project': {
            'Rank' : 1,
            'contest' : 1,
            '_id': 0
        }
    }]))
    x=[]
    y=[]
    bestRank = 100000
    bestIdx = 0
    if(duration == 'recent'):
        idx = 0
        for data in range(len(result)-1,len(result)-6,-1):
            x.append(result[data]['contest'])
            y.append(result[data]['Rank'])
            if(result[data]['Rank'] < bestRank):
                bestRank = result[data]['Rank']
                bestIdx = idx
            idx+=1
    # # bar visualization
    plt.bar(x,y,label = userName)
    plt.xlabel('contest')
    plt.ylabel('rank')
    plt.legend()
    plt.savefig(fname='bar')
    # print("res=",result)
    # [0][platform]
    # res=[]
    # for contest in result:
    #     data = [contest['contest_id'],contest['contest_rank']]
    #     res.append(data)
    # res=sorted(res)
    # # print(res)
    # elif(duration == 'alltime'):
    #     for data in range(0,len(res)):
    #         x.append(res[data][0])
    #         y.append(res[data][1])
    #         if(res[data][1] < bestRank):
    #             bestRank = res[data][1]
    #             bestIdx = data
    # # Pie chart visualization
    # # plt.pie(y,labels= x )
    # # # plt.bar(x[bestIdx], y[bestIdx], 'ro')
    # # plt.xlabel('contest')
    # # plt.ylabel('rank')
    # # # plt.legend()
    # # plt.title(f'{userName} {duration} rankings graph')
    # # plt.savefig(fname='pie')
    # # plt.close()

    # # plot visualization
    # plt.plot(x,y)
    # # plt.plot(x[bestIdx], y[bestIdx], 'ro')
    # plt.xlabel('contest')
    # plt.ylabel('rank')
    # plt.legend()
    # # # plt.title(f'{userName} {duration} rankings graph')
    # plt.savefig(fname='plot')
    # plt.close()

def graphsGenerationComparision(userName1,userName2,duration):
    result1 = list(collection.aggregate([{
        '$match': {
            'Username': userName1
        }
    }, {
        '$project': {
            'Rank' : 1,
            'contest' : 1,
            '_id': 0
        }
    }]))
    x=[]
    y=[]
    bestRank = 100000
    bestIdx = 0
    if(duration == 'recent'):
        idx = 0
        for data in range(len(result1)-1,len(result1)-6,-1):
            x.append(result1[data]['contest'])
            y.append(result1[data]['Rank'])
            if(int(result1[data]['Rank']) < int(bestRank)):
                bestRank = result1[data]['Rank']
                bestIdx = idx
            idx+=1
    result2 = list(collection.aggregate([{
        '$match': {
            'Username': userName2
        }
    }, {
        '$project': {
            'Rank' : 1,
            'contest' : 1,
            '_id': 0
        }
    }]))
    # x=[]
    y1=[]
    bestRank = 100000
    bestIdx = 0
    if(duration == 'recent'):
        idx = 0
        for data in range(len(result2)-1,len(result2)-6,-1):
            # x.append(result2[data]['contest'])
            y1.append(result2[data]['Rank'])
            if(int(result2[data]['Rank']) < int(bestRank)):
                bestRank = result2[data]['Rank']
                bestIdx = idx
            idx+=1
    x_axis = np.arange(len(x))
    plt.title(f'{userName1} vs {userName2} {duration} rankings graph')
    plt.bar(x_axis-0.2,y,width=0.4,label=userName1)
    plt.bar(x_axis+0.2,y1,width=0.4,label=userName2)
    plt.xticks(x_axis,x)
    plt.legend()
    # plt.show()
    plt.savefig(fname='bar')
    plt.close()

def graphGenerationUser(userName,duration):
    graphsGeneration(userName,duration)
    plt.title(f'{userName} {duration} rankings graph')
    plt.close()

# overallStats('Codechef','sayi_hrudai')
# graphsGeneration('sayi_hrudai','recent')
graphsGenerationComparision('sayi_hrudai','nikola_tesla_7','recent')
# client.close()
