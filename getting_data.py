import requests
from bs4 import BeautifulSoup
from datetime import datetime


day_dict = {0: 'Понедельник', 1: 'Вторник', 2: 'Среда', 3: 'Четверг', 4: 'Пятница', 5: 'Суббота', }
today = day_dict[datetime.today().weekday()]


requests.packages.urllib3.disable_warnings()
response = requests.get('https://r.sf-misis.ru/group/9', verify=False)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')

table = soup.find('table')
rows = table.find_all('tr')[1:-2]

for row in rows:
    if today in row.get_text():

        break
