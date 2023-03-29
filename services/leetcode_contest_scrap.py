from pymongo import MongoClient
from bs4 import BeautifulSoup
import certifi
import requests 
import re


client = MongoClient('mongodb+srv://19l31a0581:fenA5B7Qr9FtFjw5@cluster0.9mhf5ll.mongodb.net/test', tlsCAFile=certifi.where()) 
db = client['contestDetails']
collection = db['leetcode_users']

users = []

def getUsers():
    try:
        cursor = collection.find({}) 
        for doc in cursor:
            users.append(doc)
    except: 
        print('Some error occurred in getting the users') 

def getData(contestName, userName):
    print(userName)
    url = "https://clist.by/standings/{}/?search={}".format(contestName, userName) 
    response = requests.get(url) 
    print(response)

    soup = BeautifulSoup(response.content, 'html.parser')

    userDetails = []

    empty = soup.find('div', class_='alert-info')
    if empty != None: 
        if empty.text.strip() == 'Empty data':
            return userDetails

    rank = soup.find('td', class_='place-cell')
    if rank != None:
     userRank = rank.text.strip().split()[0]
     userDetails.append(userRank) 
    
    userDetails.append(userName)
    
    score_cell = soup.find('td', class_='score-cell') 
    if score_cell != None:
        div_tag = score_cell.find('div') 
        if div_tag != None: 
            score = div_tag.text.strip()
            userDetails.append(score) 
    
    addition_penalty_cell = soup.find('td', class_='addition-penalty-cell') 
    if addition_penalty_cell != None: 
        span = addition_penalty_cell.find_all('span') 
        userDetails.append(span[-1].text.strip())
    
    problems = soup.find_all('td', class_='problem-cell') 
    if problems != None: 
        for i in range(4):
            small1 = problems[i].find('small') 
            if small1 != None: 
                div_tag = small1.find('div') 
                if div_tag != None: 
                    userDetails.append(div_tag.text.strip())
            else:
                userDetails.append('-') 

    return userDetails


def add_to_database(userDetails, userName, contestName):
    print(userName)
    lc = db['leetcode_contests_ranklists']
    existing_doc = lc.find_one({'userName': userName})

    if existing_doc: 
        return 
    
    doc = {
            'rank': '',
            'contestName': contestName,
            'userName': userName, 
            'score': '', 
            'penalty': '', 
            'problems': []
        }
    if len(userDetails) == 0:
        lc.insert_one(doc)
        return
    
    else: 
        doc['rank'] = int(userDetails[0]) 
        doc['score'] = int(userDetails[2]) 
        doc['penalty'] = userDetails[3]
        doc['problems'] = [userDetails[4], userDetails[5], userDetails[6], userDetails[7]]
    
    lc.insert_one(doc)
        

    
def scrapeData(contestName):
    lc = db['leetcode_contests_ranklists']
    for user in users: 
        if user['url'].startswith('https'):
            match = re.search(r"/([^/]+)/$", user['url'])
            if match: 
                userName = match.group(1)
                existing_doc = lc.find_one({'userName': userName})
                if existing_doc: 
                    pass 
                else:
                    userDetails = getData(contestName, userName)
                    add_to_database(userDetails, userName, contestName)


getUsers() 
scrapeData('weekly-contest-337')



