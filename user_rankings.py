import pandas as pd
from pymongo import MongoClient, ASCENDING, errors
from openpyxl import Workbook
from openpyxl.reader.excel import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
collection = db['ranklists']

def user_ranklist(username):
    data = list(collection.aggregate([
        {'$match':
            {
                'Username': username
            }
        },
        {
            '$sort' :
                {
                    'contest' : 1
                }
        },
        {
            '$project':
                {
                    '_id': 0,
                    'Rank': 1,
                    'Username': 1,
                    'Total score': 1,
                    'Total time': 1,
                    'contest' : 1,
                    'division' : 1
                }
        }
    ]))
    print(data)
    df = pd.DataFrame(data)
    wb = Workbook()
    ws = wb.active
    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)

    # Save the workbook to a file
    wb.save('ranklist.xlsx')


# user_ranklist('sayi_hrudai')