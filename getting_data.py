import bs4.element
import requests
from bs4 import BeautifulSoup
from datetime import datetime


# приводит строку к читабельному виду
def replace_excess(string: str) -> str:
    string = string.replace('\n', '').replace('\t', '').replace('\r', '')
    return string


# используется, если пары нет
def table_empty():
    return '-'


# используется, если у всех подгрупп 1 пара
def table_single(soup: bs4.element.Tag):
    lesson_name = soup.find(class_='table-subject')
    return lesson_name.get_text().strip()


# используется, если у разных подгрупп разные пары
def table_subgroups(soup: bs4.element.Tag):
    result = {}

    # из за особенностей сайта, пришлось делать костыли
    lessons_count = len(soup.find_all(class_='table-subject'))
    subgroups_count = len(soup.find_all(class_='table-sg-name'))
    for i in range(1, subgroups_count + 1):
        result[f'{i} подгруппа'] = '-'

    subgroups = soup.find_all(class_='table-subgroup-item')[::-1]

    for i in range(lessons_count):
        result[subgroups[i].find(class_='table-sg-name').get_text()] = replace_excess(subgroups[i].find(
            class_='table-subject').get_text())

    return result


# получение сегодняшнего дня недели
def get_today():
    day_dict = {0: 'Понедельник', 1: 'Вторник', 2: 'Среда', 3: 'Четверг', 4: 'Пятница', 5: 'Суббота', }
    today = day_dict[datetime.today().weekday()]

    return today


# получение расписания группы на сегодняшний день
def get_group_schedule(group_id: int) -> tuple:
    result = []

    requests.packages.urllib3.disable_warnings()
    response = requests.get(f'https://r.sf-misis.ru/group/{group_id}', verify=False)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    table = soup.find('table')
    rows = table.find_all('tr')[1:-2]

    for row in rows:
        if get_today() in row.get_text():
            today_schedule = row.find_all('td')
            break

    # проверка типа занятия и получение результата
    for i in today_schedule:
        if i.get('class')[0] == 'table-empty':
            result.append(table_empty())

        if i.get('class')[0] == 'table-single':
            result.append(table_single(i))

        if i.get('class')[0] == 'table-subgroups':
            result.append(table_subgroups(i))

    return tuple(result)


# для использования скрипта, необходимо вызвать функцию get_group_schedule(group_id), в качестве аргумента - номер группы
# например - get_group_schedule(9)
print(get_group_schedule(9))
