from openpyxl.reader.excel import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from pymongo import MongoClient
import certifi
import pandas as pd
from openpyxl import Workbook 
from openpyxl.styles import PatternFill, Alignment, Side, Border




client = MongoClient('mongodb+srv://19l31a0581:fenA5B7Qr9FtFjw5@cluster0.9mhf5ll.mongodb.net/test', tlsCAFile=certifi.where())
db = client['contestDetails']
collection = db['ranklists']


def convert_to_excel(contest_id):
    # Retrieve all data from the collection
    divisions = ['Div A','Div B','Div C','Div D']
    for div in divisions:
        data = list(collection.aggregate([
            {'$match':
                 {
                     'contest': contest_id,
                     'division': div
                 }
            },
            {
                '$sort' : {'Rank' : 1}
            },
            {
                '$project' :
                    {
                        '_id' :0,
                        'Rank' : 1,
                        'Username' : 1,
                        'Total score' : 1,
                        'Total time' : 1
                    }
            }
        ]))
        # print("data=",data)
        userCollection = db['users']
        for user in data : 
            username = user['Username']
            rollnumber = '-'
            try:
                rollnumber = list(userCollection.find({'codechefId' : username}))[0]['collegeId']
            except:
                pass
            user['Roll number'] = rollnumber
        # print('div=',div)
        # print("total_cout=",data)
        # Convert the data to a DataFrame
        df = pd.DataFrame(data)

        # Create a new Excel workbook and add the DataFrame to a new worksheet
        wb = Workbook()
        try:
            wb = load_workbook('ranklist.xlsx')
        except:
            wb = Workbook()
            wb.save('ranklist.xlsx')
        try:
            del wb['Sheet']
        except:
            pass
        try:
            del wb[div]
            wb.create_sheet(div)
        except:
            wb.create_sheet(div)
        ws = wb[div]
        for r in dataframe_to_rows(df, index=False, header=True):
            # print("r=",r)
            ws.append(r)

        # Save the workbook to a file
        for col in ws.columns: 
            for cell in col:
                alignment_obj = cell.alignment.copy(horizontal='center', vertical='center')
                cell.alignment = alignment_obj
        double = Side(border_style="double", color="000000")
        ws['A1'].fill = PatternFill('solid', fgColor='FFFF00')
        ws['A1'].alignment = Alignment(horizontal='center')
        ws['A1'].border = Border(top=double, left=double, right=double, bottom=double)
        ws.column_dimensions['A'].width = 20

        ws['B1'].fill = PatternFill('solid', fgColor='FFFF00')
        ws['B1'].alignment = Alignment(horizontal='center')
        ws['B1'].border = Border(top=double, left=double, right=double, bottom=double)
        ws.column_dimensions['B'].width = 20

        ws['C1'].fill = PatternFill('solid', fgColor='FFFF00')
        ws['C1'].alignment = Alignment(horizontal='center')
        ws['C1'].border = Border(top=double, left=double, right=double, bottom=double)
        ws.column_dimensions['C'].width = 20

        ws['D1'].fill = PatternFill('solid', fgColor='FFFF00')
        ws['D1'].alignment = Alignment(horizontal='center')
        ws['D1'].border = Border(top=double, left=double, right=double, bottom=double)
        ws.column_dimensions['D'].width = 20

        ws['E1'].fill = PatternFill('solid', fgColor='FFFF00')
        ws['E1'].alignment = Alignment(horizontal='center')
        ws['E1'].border = Border(top=double, left=double, right=double, bottom=double)
        ws.column_dimensions['E'].width = 20
        
        wb.save('ranklist.xlsx')


def check_if_contest_exists_in_db(contest_id):
    data = list(collection.aggregate([
        {
            '$match' : {
                'contest' : contest_id
            }
        }
    ]))
    if(len(data)!=0):
        return 1
    return 0

# convert_to_excel("START78")