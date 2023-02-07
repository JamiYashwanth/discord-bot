from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from openpyxl import Workbook
from bs4 import BeautifulSoup


url = "https://www.codechef.com/rankings/START76B?filterBy=Institution%3DVignan%27s%20Institute%20Of%20Information%20Technology%2C%20Visakhapatnam&itemsPerPage=100&order=asc&page=1&sortBy=rank"

# initiating the webdriver. Parameter includes the path of the webdriver.
driver = webdriver.Chrome('./chromedriver')
driver.get(url)
time.sleep(10)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
u=soup.find_all('tr',class_='MuiTableRow-root')
user_data=[]
for user_list in u:
    user = []
    username = user_list.find('span',class_="m-username--link")
    userRank = user_list.find('p',class_="MuiTypography-root")
    if((username != None)):
        user.append(username.text)
        user.append(userRank.text)
        user_data.append(user)
print(user_data)

wb=Workbook()
ws = wb.active

for data in user_data:
    ws.append(data)

wb.save("rankings.xlsx")
