import os
from scraping import *

# contest_id = 'COOK'
recentContestId = 144

# for contest_id in range (1,recentContestId+1):
contest_type = 'START'
contest_id = '34'
scrape(f'{contest_type}{contest_id}', 'A')
scrape(f'{contest_type}{contest_id}', 'B')
scrape(f'{contest_type}{contest_id}', 'C')
scrape(f'{contest_type}{contest_id}', 'D')
print(f'Generated {contest_type}{contest_id} sheet')
        # print(contest_id)
# print(isExisting)