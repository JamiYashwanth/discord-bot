import openpyxl
import os
from user_model import *

path = 'C:/Users/jamiy/PycharmProjects/pythonProject/contests_ranklists'
dir_list = os.listdir(path)
# print(dir_list)

for contest in dir_list:
    contest_id = contest.split('_')[0]
    excle = openpyxl.load_workbook(f'C:/Users/jamiy/PycharmProjects/pythonProject/contests_ranklists/{contest_id}_rankings.xlsx')
    divisions = ['Div A','Div B','Div C','Div D']
    for division in divisions:
        divExcle = excle[division]
        for row in range(2, divExcle.max_row + 1):
            contestRank = int(divExcle[row][0].value)
            userName = divExcle[row][1].value
            totalScore = int(divExcle[row][2].value)
            totalTime = divExcle[row][3].value
            # print("rank=",type(int(contestRank)))
            # break
            updateToDb(userName, contest_id, contestRank, division, 'Codechef', totalScore, totalTime)

print("Succesfully uploaded to database")