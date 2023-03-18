import pandas as pd
from pymongo import MongoClient, ASCENDING, errors

def excle_to_db(contest_type,contest_id,division):
    df = pd.read_excel(f'C:/Users/jamiy/PycharmProjects/pythonProject/contests_ranklists/{contest_type}{contest_id}_rankings.xlsx', sheet_name=division)
    data = df.to_dict('records')

    for row in data:
        row['contest'] = f'{contest_type}{contest_id}'
        row['division'] = division

    print(data)

    client = MongoClient('mongodb://localhost:27017/')
    db = client['mydatabase']
    collection = db['ranklists']

    index_name = "user_contest_and_division_as_index"
    index_fields = [("Username",ASCENDING),("contest", ASCENDING), ("division", ASCENDING)]
    index_options = {
        'unique': True,
        'name': index_name
    }
    try:
        collection.create_index(index_fields, **index_options)
    except errors.OperationFailure as e:
        print(f"Index creation failed: {e.details['errmsg']}")

    try:
        result = collection.insert_many(data)
    except:
        print("already exists")
    # print(result.inserted_ids)

def data_into_db(user_data):
    print('userData=',user_data)
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mydatabase']
    collection = db['ranklists']

    index_name = "user_contest_and_division_as_index"
    index_fields = [("Username", ASCENDING), ("contest", ASCENDING), ("division", ASCENDING)]
    index_options = {
        'unique': True,
        'name': index_name
    }
    try:
        collection.create_index(index_fields, **index_options)
    except errors.OperationFailure as e:
        print(f"Index creation failed: {e.details['errmsg']}")

    try:
        result = collection.insert_many(user_data)
        print(f'successfully inserted into db')
    except:
        print("already exists")



