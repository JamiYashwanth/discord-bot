import os
from scraping import *

# contest_id = 'Start52'
recentContestId = 74

for contest_id in range (1,recentContestId+1):
    contest_type = 'START'
    path = f'C:/Users/jamiy/PycharmProjects/pythonProject/contests_ranklists/{contest_type}{contest_id}_rankings.xlsx'
    isExisting = os.path.exists(path)
    # print(isExisting)
    if(not isExisting):
        scrape(f'{contest_type}{contest_id}', 'A')
        scrape(f'{contest_type}{contest_id}', 'B')
        scrape(f'{contest_type}{contest_id}', 'C')
        scrape(f'{contest_type}{contest_id}', 'D')
        print(f'Generated {contest_type}{contest_id} sheet')
        # print(contest_id)
# print(isExisting)