from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from openpyxl import Workbook,load_workbook
from bs4 import BeautifulSoup



def scrape(contest_id,div):
    url = f'https://www.codechef.com/rankings/{contest_id + div}?filterBy=Institution%3DVignan%27s%20Institute%20Of%20Information%20Technology%2C%20Visakhapatnam&itemsPerPage=100&order=asc&page=1&sortBy=rank'
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome('./chromedriver',options=op)
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
            user.append(userRank.text)  # rank
            user.append(username.text)  # username
            user.append((row[2].text)[11:])  # total score
            user.append((row[3].text)[7:])  # total time
            user_data.append(user)

    try:
        wb=load_workbook(f'{contest_id}_rankings.xlsx')
    except:
        wb = Workbook()
        wb.save(f'{contest_id}_rankings.xlsx')
    try:
        wb[f'Div {div}']
    except:
        wb.create_sheet(f'Div {div}')
    ws = wb[f'Div {div}']
    ws.delete_rows(0, ws.max_row - 1)
    row = ['Rank', 'Username', 'Total score', 'Total time']
    ws.append(row)
    if len(user_data) > 0:
        for data in user_data:
            ws.append(data)
    wb.save(filename=f'{contest_id}_rankings.xlsx')


