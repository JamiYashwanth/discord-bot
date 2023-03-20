from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from pymongo import MongoClient, ASCENDING, errors
from selenium.webdriver.common.keys import Keys
import time
from openpyxl import Workbook, load_workbook
from bs4 import BeautifulSoup
# from test import *
from convert_mongodata_to_excle import *
client = MongoClient('mongodb+srv://19l31a0581:fenA5B7Qr9FtFjw5@cluster0.9mhf5ll.mongodb.net/test')
db = client['contestDetails']
collection = db['ranklists']


def data_into_db(user_data):
    # print("userData=",user_data)

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
        collection.insert_many(user_data)
    except:
        pass

def scrape_page(url,contest_id,div):
    # print(f'scraping {url}')
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome('./chromedriver', options=op)
    driver.get(url)
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    u = soup.find_all('tr', class_='MuiTableRow-root')
    user_data = []
    for user_list in u:
        user = []
        username = user_list.find('span', class_="m-username--link")
        userRank = user_list.find('p', class_="MuiTypography-root")
        row = user_list.find_all('td', class_="MuiTableCell-root")
        if ((username != None)):
            user = {
                'Rank': userRank.text,
                'Username': username.text,
                'Total score': (row[2].text)[11:],
                'Total time': (row[3].text)[7:],
                'contest': contest_id,
                'division': f'Div {div}'
            }
            user_data.append(user)
    data_into_db(user_data)

def scrape(contest_id, div):
    checkIfAlreadyScraped = len(list(collection.find({'contest' : contest_id,'division' : f'Div {div}'})))
    # print(f'{contest_id} {div} {checkIfAlreadyScraped}')
    if(checkIfAlreadyScraped == 0):
        # print("entered")
        with ThreadPoolExecutor(max_workers=5) as executor:
            urls = [
                f'https://www.codechef.com/rankings/{contest_id + div}?filterBy=Institution%3DVignan%27s%20Institute%20Of%20Information%20Technology%2C%20Visakhapatnam&itemsPerPage=100&order=asc&page={pageNo}&sortBy=rank'
                for pageNo in range(1, 6)
            ]
            futures = [executor.submit(scrape_page(url,contest_id,div), url) for url in urls]
            for future in as_completed(futures):
                pass
        print(f'Succesfully scraped {contest_id}{div} and inserted into db')

def scrape_all_contests():
    contest_type = 'START'
    division = ['A', 'B', 'C', 'D']
    with ThreadPoolExecutor(max_workers=4) as executor:
        for contest_id in range(38, 39):
            print(f'Scraping {contest_type}{contest_id} in progress...')
            for div in division:
                executor.submit(scrape, contest_type + str(contest_id), div)
    print("Successfully scraped and inserted to db")

# scrape_all_contests()
